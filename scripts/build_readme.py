#!/usr/bin/env python3
"""Generate the marker-bounded blocks of the profile README from the site's
sources of truth (zaherkarp.github.io).

The GitHub profile README's Title, Stack, Writing, and Research blocks are
generated artifacts of the site's single sources of truth, so the profile
cannot quietly drift from the site. Featured projects joined them on
2026-09-12, after the hand-written version drifted into a 404, a plain-HTTP
redirect chain and a two-projects-stale list. The remaining prose blocks
(About, Selected impact, Education) are hand-authored and left untouched.

Sources (inside the site checkout passed via --site):
  src/content/resume.md          -> headline title + employer (current role)
  src/content/skills.yaml        -> stack badges
  src/content/blog/*.md          -> featured writing (frontmatter)
  src/content/projects.yaml      -> featured projects list
  src/content/publications.yaml  -> research highlights

Idempotent: same inputs -> byte-identical README. Mirrors the site's
scripts/build_portfolio.py replace_between() marker injection.

Usage:
  python scripts/build_readme.py --site path/to/zaherkarp.github.io
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import frontmatter
import yaml

# Profile-level social URLs (stable; not stored on the site as data).
SCHOLAR = "https://scholar.google.com/citations?user=exrRbXMAAAAJ"
RESEARCHGATE = "https://www.researchgate.net/profile/Zaher-Karp"
# Canonical host is www; the apex 301s to it (site CLAUDE.md, "Canonical URLs
# are www"). Linking the apex spends a redirect on every click, so both
# bases below are www. BLOG_BASE said apex until 2026-09-12.
SITE_BASE = "https://www.zaherkarp.com"
BLOG_BASE = f"{SITE_BASE}/blog"

WRITING_COUNT = 5  # most-recent non-draft posts shown under Writing


# --------------------------------------------------------------------------
# Marker injection (mirrors build_portfolio.replace_between: regex, DOTALL,
# warn-and-skip on a missing marker, comment lines preserved).
# --------------------------------------------------------------------------
def replace_between(text: str, marker: str, payload: str, end_indent: str = "") -> str:
    pat = re.compile(
        rf"(<!--\s*{re.escape(marker)}:start\s*-->)(.*?)(<!--\s*{re.escape(marker)}:end\s*-->)",
        re.DOTALL,
    )
    if not pat.search(text):
        print(f"  WARN: marker {marker}:start/end not found; skipping", file=sys.stderr)
        return text
    return pat.sub(lambda m: f"{m.group(1)}\n{payload}\n{end_indent}{m.group(3)}", text)


# --------------------------------------------------------------------------
# shields.io badge helpers (flat-square; label encoding: '_'->'__', '-'->'--',
# ' '->'_'). Kept churn-free so re-runs produce byte-identical output.
# --------------------------------------------------------------------------
def _enc(s: str) -> str:
    return s.replace("_", "__").replace("-", "--").replace(" ", "_")


def _badge(label: str, color: str, logo: str | None = None) -> str:
    url = f"https://img.shields.io/badge/{_enc(label)}-{color}?style=flat-square"
    if logo:
        url += f"&logo={logo}&logoColor=white"
    return f"![{label}]({url})"


# Category -> badge background. Uses the site palette (teal accent + two cool
# neutrals) for brand coherence.
CAT_COLOR = {
    "Engineering & data": "0A5C54",
    "Cloud & BI": "334155",
    "Healthcare": "6A6A6A",
}

# skills.yaml `id` -> list of (badge label, shields logo slug or None).
# Presentation only: which skills exist, their order, and their category all
# come from skills.yaml. A skill id absent here still renders (label derived
# from its name, no logo), so a newly added skill appears automatically.
SKILL_BADGES: dict[str, list[tuple[str, str | None]]] = {
    "sql": [("SQL", None)],
    "python": [("Python", "python")],
    "dbt": [("dbt", "dbt")],
    "rails": [("Ruby on Rails", "rubyonrails")],
    "clojure": [("Clojure", "clojure")],
    "perl": [("Perl", "perl")],
    "sas": [("SAS", None)],
    "stata": [("Stata", None)],
    "r": [("R", "r")],
    "git": [("git", "git")],
    "aws": [("AWS", "amazonwebservices")],
    "azure-databricks": [("Azure", "microsoftazure"), ("Databricks", "databricks")],
    "okta": [("Okta", "okta")],
    "sisense": [("Sisense", None)],
    "periscope": [("Periscope", None)],
    "power-bi": [("Power BI", "powerbi")],
    "grafana": [("Grafana", "grafana")],
    "datadog": [("Datadog", "datadog")],
    "hedis": [("HEDIS", None)],
    "stars": [("CMS Medicare Stars", None)],
    "aco-mssp": [("ACO", None), ("MSSP", None)],
    "hipaa": [("HIPAA", None)],
    "hitrust": [("HITRUST", None)],
    "icd10": [("ICD-10", None)],
    "rxnorm": [("RxNorm", None)],
    "hl7": [("HL7", None)],
    "epic": [("Epic", None)],
    "cerner": [("Cerner", None)],
    "veradigm": [("Veradigm", None)],
    "athenahealth": [("athenahealth", None)],
}


def _fallback_label(name: str) -> str:
    """Short badge label from a verbose skills.yaml name (drop parenthetical /
    slash detail): 'Python (pandas, PySpark)' -> 'Python'."""
    return re.split(r"[(/]", name)[0].strip()


def render_title(site: Path) -> str:
    """Headline `<strong>Title</strong> · Employer` from the resume's current
    ('Present') role. Matches the two-space indent of the centered <p>."""
    text = (site / "src/content/resume.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    role_re = re.compile(r"^\*\*(.+?)\*\*\s*\|\s*(.+?)\s*$")
    for i, ln in enumerate(lines):
        m = role_re.match(ln)
        if not m:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        date_ln = lines[j] if j < len(lines) else ""
        if "Present" in date_ln:
            employer, title = m.group(1).strip(), m.group(2).strip()
            return f"  <strong>{title}</strong> · {employer}"
    raise SystemExit("build_readme: no current ('Present') role found in resume.md")


def render_stack(site: Path) -> str:
    data = yaml.safe_load((site / "src/content/skills.yaml").read_text(encoding="utf-8"))
    order = data.get("categories_order") or []
    skills = data.get("skills") or []
    by_cat: dict[str, list[dict]] = {c: [] for c in order}
    for sk in skills:
        by_cat.setdefault(sk["category"], []).append(sk)
    rows = []
    for cat in order:
        color = CAT_COLOR.get(cat, "6A6A6A")
        badges = []
        for sk in by_cat.get(cat, []):
            specs = SKILL_BADGES.get(sk["id"]) or [(_fallback_label(sk["name"]), None)]
            for label, logo in specs:
                badges.append(_badge(label, color, logo))
        rows.append(f"**{cat}**  \n" + " ".join(badges))
    return "\n\n".join(rows)


def render_writing(site: Path, n: int = WRITING_COUNT) -> str:
    """Top-n most-recent non-draft posts, mirroring the site's load_posts:
    sorted glob, skip `_`-prefixed files and drafts, require a publishDate,
    tie-break on filename."""
    posts = []
    for p in sorted((site / "src/content/blog").glob("*.md")):
        if p.stem.startswith("_"):
            continue
        fm = frontmatter.load(p)
        if fm.metadata.get("draft"):
            continue
        d = fm.metadata.get("publishDate")
        if not d:
            continue
        ds = d.isoformat() if hasattr(d, "isoformat") else str(d)
        title = str(fm.metadata.get("title", "")).strip()
        if not title:
            continue
        posts.append((ds, p.stem, title))
    posts.sort(key=lambda t: t[0], reverse=True)  # stable: ties keep filename order
    lines = []
    for _ds, slug, title in posts[:n]:
        title = title.replace("—", ",")  # em-dash -> comma (chrome convention)
        lines.append(f"- [{title}]({BLOG_BASE}/{slug}/)")
    return "\n".join(lines)


def _display_label(label: str) -> str:
    """Sentence-case a link label for the profile.

    Labels are stored in the YAML exactly as index.html writes them, because
    the site's lint_projects compares the two literally. The site's own rows
    are lowercase by its typographic convention ("post", "case study"), which
    reads as a typo in a README list. This capitalises the first character
    and touches nothing else, so "GitHub" survives intact where a .title() or
    .capitalize() would mangle it to "Github". Presentation only: do NOT push
    this back into the YAML or the site lint stops matching.
    """
    return label[:1].upper() + label[1:] if label else label


def render_projects(site: Path) -> str:
    """The Featured projects list, from the site's src/content/projects.yaml.

    That file is the site's canonical project LIST and is held against
    index.html's actual project cards by its scripts/lint_projects.py, so
    this block cannot drift from the site the way the hand-written list it
    replaces did. Before 2026-09-12 this section was authored here by hand
    and had gone wrong three ways at once: a [Source] link to
    zaherkarp.github.io, private since 2026-08-28 and so a 404 on the front
    page anyone lands on when they look him up; a [Live feed] pointing at the
    retired /medicare-advantage-insight-engine/ subpath, whose redirect chain
    then terminated on plain HTTP; and a list two projects behind the site
    while promoting one the site does not treat as a project at all.

    URLs are stored site-relative in the YAML exactly as index.html writes
    them ("/blog/..."), which is what lets the site's lint compare the two
    surfaces literally. Absolutising them is therefore THIS side's job, and
    it must stay that way: storing absolute URLs in the YAML would silence
    that lint.
    """
    data = yaml.safe_load((site / "src/content/projects.yaml").read_text(encoding="utf-8"))
    entries = sorted((data or {}).get("projects") or [], key=lambda e: e.get("order", 0))

    def absolutise(url: str) -> str:
        return f"{SITE_BASE}{url}" if url.startswith("/") else url

    lines = []
    for e in entries:
        # Em-dash -> comma on sourced text, the same chrome convention
        # render_writing applies to post titles. The " — " separator below is
        # the generator's own punctuation, matching render_research.
        title = str(e.get("title", "")).strip().replace("\u2014", ",")
        summary = " ".join(str(e.get("summary", "")).split()).replace("\u2014", ",")
        links = " · ".join(
            f"[{_display_label(l['label'])}]({absolutise(l['url'])})"
            for l in (e.get("links") or [])
        )
        # Two trailing spaces = a markdown hard break, so the links sit on
        # their own line under the description, as the hand-written block did.
        lines.append(f"- **{title}** — {summary}  \n  {links}")
    return "\n".join(lines)


def render_research(site: Path) -> str:
    pubs = yaml.safe_load((site / "src/content/publications.yaml").read_text(encoding="utf-8"))
    n = len(pubs)
    ranked = sorted(pubs, key=lambda e: e.get("citations", 0) or 0, reverse=True)[:2]
    lines = [
        f"{n} peer-reviewed publications ([Google Scholar]({SCHOLAR}), "
        f"[ResearchGate]({RESEARCHGATE})). The two most cited:",
        "",
    ]
    for e in ranked:
        url = e["links"][0]["url"] if e.get("links") else ""
        title = str(e["title"]).strip()
        venue = str(e.get("venue", "")).strip()
        year = e.get("year", "")
        link = f"[{title}]({url})" if url else title
        lines.append(f"- {link} — *{venue}* ({year})")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--site", required=True, help="path to a zaherkarp.github.io checkout")
    ap.add_argument("--readme", default="README.md")
    args = ap.parse_args()

    site = Path(args.site)
    readme = Path(args.readme)
    text = readme.read_text(encoding="utf-8")

    text = replace_between(text, "title", render_title(site), end_indent="  ")
    text = replace_between(text, "stack", render_stack(site))
    text = replace_between(text, "writing", render_writing(site))
    text = replace_between(text, "projects", render_projects(site))
    text = replace_between(text, "research", render_research(site))

    readme.write_text(text, encoding="utf-8")
    print("build_readme: wrote", readme)


if __name__ == "__main__":
    main()
