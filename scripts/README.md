# Profile README build

The blocks in the profile [`README.md`](../README.md) marked `Title`, `Stack`,
`Writing`, `Projects`, and `Research` are **generated** from
[zaherkarp.github.io](https://github.com/zaherkarp/zaherkarp.github.io)'s
sources of truth, so this profile cannot drift from the site. Everything else in
the README (About, Selected impact, Education) is hand-written prose the
generator never touches.

`Projects` joined them on 2026-09-12. It had been hand-written, and by then it
had drifted three ways at once: a `[Source]` link to a repo that went private on
2026-08-28, so a 404 on the first page anyone sees when they look him up; a
`[Live feed]` pointing at a retired subpath whose redirect chain terminated on
plain HTTP; and a list two projects behind the site while promoting one the site
does not treat as a project at all. Dead links were the symptom; having no source
of truth was the cause.

## Files

| File | What it does |
| --- | --- |
| `build_readme.py` | Reads the site's sources and regenerates the five marked blocks in `README.md`. Idempotent: the same inputs produce byte-identical output. |
| `lint_markers.py` | Fails if the five `<!-- name:start -->` / `<!-- name:end -->` marker pairs go missing, crossed, or unterminated, so a stray edit can't corrupt a block or make the generator silently no-op. |
| `check_badges.py` | Renders every badge and fails if a requested icon does not draw or a link is gone. Stdlib only. See Troubleshooting. |
| `requirements.txt` | `pyyaml` + `python-frontmatter`, the only dependencies. |

## What feeds what

Each block is a projection of one source of truth on the site:

| Block | Source (in `zaherkarp/zaherkarp.github.io`) |
| --- | --- |
| Title | `src/content/resume.md`, the current ("Present") role |
| Stack | `src/content/skills.yaml` (categories + skills) |
| Writing | `src/content/blog/*.md` frontmatter (recent non-draft posts) |
| Projects | `src/content/projects.yaml` (the site's canonical project list) |
| Research | `src/content/publications.yaml` (count + most-cited) |

## Running it by hand

The sync runs on its own (see Automation). To run it locally, clone the site
somewhere and point the generator at it. The site repo is **private**, so this
needs a GitHub login with access to it (`gh auth login`, an SSH key, or a
credential helper):

```bash
git clone --depth 1 git@github.com:zaherkarp/zaherkarp.github.io.git site
pip install -r scripts/requirements.txt
python scripts/build_readme.py --site site
python scripts/lint_markers.py
```

Re-running with unchanged inputs leaves `README.md` byte-identical.

## Automation

Three workflows:

| Workflow | When | What |
| --- | --- | --- |
| `sync-readme.yml` | daily 08:00 UTC, manual, on script changes | Clones the site, regenerates the blocks, commits only on change. |
| `lint.yml` | every pull request and push | `lint_markers.py`. |
| `check-badges.yml` | weekly Monday, manual, on README or script changes | `check_badges.py --self-test`, then `check_badges.py`. |

**One secret.** The site repo has been private since 2026-08-28, so the sync
reads it with `SITE_READ_TOKEN`, a fine-grained PAT with read-only Contents
access to `zaherkarp/zaherkarp.github.io`. Fine-grained PATs expire. When it
lapses the sync's preflight step fails with a message saying so; reissue the
token and update the secret. The write side commits to this repo with the
built-in `GITHUB_TOKEN`. (This section said "no secrets, the read side is a
public repo" until 2026-10-12, which stopped being true when the site went
private.)

## Do not hand-edit the generated blocks

Anything between the five marker pairs in `README.md` is overwritten on the next
sync. Change the content at its source on the site instead. Because the
generator reads the site's field names (`skills.yaml` keys, `publications.yaml`
fields, the resume's `**Employer** | Title` + "Present" shape), a schema rename
on the site needs a matching edit to `build_readme.py` here. That contract is
documented on the site in `CLAUDE.md` under "GitHub profile README (external
consumer)", and in its `docs/pipelines.md` (pipeline 10).

## The Projects block's contract with the site

`src/content/projects.yaml` stores link URLs **site-relative**, exactly as
`index.html` writes them (`/blog/...`). That is what lets the site's own
`scripts/lint_projects.py` compare the YAML against its project cards
literally, and that lint is the thing keeping this block honest.

So absolutising those URLs is **this** repo's job, in `render_projects`, and it
must stay that way. Storing absolute URLs in the YAML would silence the site
lint and put us back where we started. `_display_label` is presentation for the
same reason: the site writes lowercase link labels by its own typographic
convention, and sentence-casing them here must not be pushed back into the YAML.

## Troubleshooting: badges with missing icons (2026-10-12)

**Symptom.** Most of the graphics on the profile looked dead: badges rendered
as plain colored boxes with no icon. Seven of them had asked for a logo and
lost it: LinkedIn, Tableau Public and Resume in the header row (hand-written),
and dbt, AWS, Azure and Power BI in the generated Tech stack block. The other
thirteen stack badges never had a logo (SQL, SAS, Stata, the healthcare
terms), so after the loss 22 of 32 stack badges and 3 of 7 header badges were
text-only boxes.

**What was ruled out first, by measurement.**

- shields.io: all 39 badge URLs returned 200 with a valid SVG.
- GitHub's image proxy (camo): all 39 proxied URLs, taken from the README as
  GitHub renders it, returned 200 `image/svg+xml`.
- The sync pipeline: `sync-readme.yml` ran green every day, and running
  `build_readme.py` against the current site produced no diff, so the
  generated content was current.
- Links: every `www.zaherkarp.com` and `signal.zaherkarp.com` link returned
  200. LinkedIn, Google Scholar and ResearchGate refuse automated clients, so
  their status says nothing either way.

**Cause.** shields.io draws logos from [Simple Icons](https://simpleicons.org),
and Simple Icons has removed these brands' icons (it drops a brand when the
brand owner objects). Checked against Simple Icons 16.35.0: `linkedin`,
`tableau`, `adobeacrobatreader`, `dbt`, `amazonwebservices`, `microsoftazure`
and `powerbi` are all absent. shields.io does not error on an unknown slug. It
returns a normal 200 badge without the icon, so no status check could see it.
The only evidence is inside the SVG: a badge that draws its logo contains an
`<image>` element, and these did not.

**Fix.**

- The dead slugs were removed: from the header row in `README.md` directly,
  and from `SKILL_BADGES` in `build_readme.py` for the stack block (set to
  `None`). The badges now render as deliberate text-only badges, matching the
  others in their row, instead of looking broken.
- `check_badges.py` now catches this class of failure. It fetches every
  badge and fails when a requested logo is not drawn, and fails on any link
  returning 404/410 or no HTTP answer. Its `--self-test` checks the LinkedIn
  badge (known dead) and the Python badge (known live) and refuses to pass
  unless it can tell them apart. Run against the pre-fix README it flagged
  exactly the seven badges above; against the fixed one it passes.

**If it fires again.** Run `python scripts/check_badges.py` locally to see
which badge failed. Check the slug at simpleicons.org. If the brand is gone,
set its logo to `None` (stack block, in `build_readme.py`) or delete the
`&logo=...&logoColor=white` part (header row, in `README.md`). Do not
substitute an unrelated icon to keep the row looking full.

**Not changed, flagged for a decision.** The badge colors are hardcoded to the
site's old petrol-teal palette (`0A5C54`, in `CAT_COLOR` and the header row).
The site moved to the "Lichen" moss-green palette on 2026-07-23 (accent
`#1d6835`, source `src/content/palette.yaml`), so the profile no longer
matches the site even though the code comment says it uses the site palette.
Reading the accent from `palette.yaml` would remove that drift for good.
