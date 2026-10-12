#!/usr/bin/env python3
"""Check that every graphic and link on the profile README still works.

Why this exists: on 2026-10-12 seven badges on the profile had lost their
icons (LinkedIn, Tableau, Resume, dbt, AWS, Azure, Power BI) and nothing had
reported it. Simple Icons, the icon set shields.io draws from, had removed
those brands, and shields.io answers an unknown `logo=` slug with an ordinary
200 badge that simply has no icon. So every status check passed while the page
looked broken. A status code cannot see this failure; only the rendered SVG
can. This script fetches each badge and checks the SVG for the icon itself.

Checks:
  1. Every shields.io badge returns 200 and is an SVG.
  2. Every badge that asks for a logo (`logo=...`) actually draws one: the
     SVG must contain an <image> element. This is the check that would have
     caught the 2026-10-12 breakage.
  3. Every outbound link resolves. A 404/410 or a DNS/connection failure is
     a hard failure. Hosts that refuse automated clients (LinkedIn, Google
     Scholar, ResearchGate) are reported as "not checkable" and never fail,
     because their answer to a bot says nothing about the page.

Usage:
  python scripts/check_badges.py              # check README.md
  python scripts/check_badges.py --self-test  # prove check 2 can fail

Stdlib only, so the workflow installs nothing. Not a pre-push lint: it needs
the network and its answer depends on third parties.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (compatible; zaherkarp-profile-check/1.0)"

# Hosts that answer automated requests with 403/429/999 regardless of whether
# the page exists. Their status is printed but never fails the run.
BOT_BLOCKED = (
    "linkedin.com",
    "scholar.google.com",
    "researchgate.net",
)

# A badge whose logo is known to have been removed from Simple Icons. Used by
# --self-test as the negative control: check 2 MUST flag it, or the check is
# not actually looking at the icon.
DEAD_LOGO_CONTROL = "https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white"
LIVE_LOGO_CONTROL = "https://img.shields.io/badge/Python-0A5C54?style=flat-square&logo=python&logoColor=white"


def fetch(url: str, attempts: int = 3) -> tuple[int | None, bytes, str]:
    """GET a URL. Returns (status, body, error). Retries 429/5xx only, with
    backoff, so a slow third party is not reported as broken. status is None
    when no HTTP answer arrived at all (DNS, TLS, timeout)."""
    delay = 2.0
    last_err = ""
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, r.read(), ""
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                last_err = f"HTTP {e.code}"
                if i < attempts - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
            return e.code, b"", f"HTTP {e.code}"
        except Exception as e:  # network-level failure: no HTTP answer
            last_err = f"{type(e).__name__}: {e}"
            if i < attempts - 1:
                time.sleep(delay)
                delay *= 2
    return None, b"", last_err


def badge_problem(url: str) -> str | None:
    """Return a description of what is wrong with a badge, or None if fine."""
    status, body, err = fetch(url)
    if status != 200:
        return f"badge did not load ({err or status})"
    svg = body.decode("utf-8", "replace")
    if "<svg" not in svg:
        return "badge response is not an SVG"
    if "logo=" in url and "<image" not in svg:
        slug = re.search(r"logo=([^&]+)", url).group(1)
        return (f"logo '{slug}' requested but not drawn "
                "(slug no longer in Simple Icons; drop it or pick another)")
    return None


def extract(readme: str) -> tuple[list[str], list[str]]:
    """Split README URLs into (badges, links), de-duplicated, in page order."""
    found = re.findall(r'(?:src="|href="|\]\()(https?://[^")\s]+)', readme)
    seen, badges, links = set(), [], []
    for u in (html.unescape(x) for x in found):
        if u in seen:
            continue
        seen.add(u)
        (badges if u.startswith("https://img.shields.io/") else links).append(u)
    return badges, links


def self_test() -> int:
    """Negative and positive control for the logo check. Exits non-zero if
    the check cannot tell a missing icon from a present one."""
    dead = badge_problem(DEAD_LOGO_CONTROL)
    live = badge_problem(LIVE_LOGO_CONTROL)
    ok = dead is not None and "not drawn" in dead and live is None
    print(f"self-test: dead-logo control flagged = {dead is not None} ({dead})")
    print(f"self-test: live-logo control clean   = {live is None} ({live})")
    print("self-test:", "ok" if ok else "FAILED (the logo check is blind)")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--readme", default="README.md")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    badges, links = extract(Path(args.readme).read_text(encoding="utf-8"))
    failures: list[str] = []

    print(f"Badges ({len(badges)})")
    for u in badges:
        problem = badge_problem(u)
        print(f"  {'FAIL' if problem else 'ok  '} {u}" + (f"\n       {problem}" if problem else ""))
        if problem:
            failures.append(f"{u}: {problem}")

    print(f"Links ({len(links)})")
    for u in links:
        if u.startswith("mailto:"):
            continue
        status, _, err = fetch(u)
        blocked = any(h in u for h in BOT_BLOCKED)
        if status is not None and status < 400:
            print(f"  ok   {status} {u}")
        elif blocked:
            print(f"  skip {status or err} {u} (host refuses automated clients)")
        elif status in (404, 410) or status is None:
            print(f"  FAIL {status or err} {u}")
            failures.append(f"{u}: {status or err}")
        else:
            # 401/403 etc. from a host not on the bot list: report, do not
            # fail, since an access answer is not evidence the page is gone.
            print(f"  warn {status} {u}")

    if failures:
        print(f"\n{len(failures)} problem(s):")
        for f in failures:
            print("  -", f)
            print(f"::error::{f}")
        return 1
    print("\nAll badges draw and all checkable links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
