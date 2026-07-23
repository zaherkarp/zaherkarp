# Profile README build

The blocks in the profile [`README.md`](../README.md) marked `Title`, `Stack`,
`Writing`, and `Research` are **generated** from
[zaherkarp.github.io](https://github.com/zaherkarp/zaherkarp.github.io)'s
sources of truth, so this profile cannot drift from the site. Everything else in
the README (About, Selected impact, Featured projects, Education) is hand-written
prose the generator never touches.

## Files

| File | What it does |
| --- | --- |
| `build_readme.py` | Reads the site's sources and regenerates the four marked blocks in `README.md`. Idempotent: the same inputs produce byte-identical output. |
| `lint_markers.py` | Fails if the four `<!-- name:start -->` / `<!-- name:end -->` marker pairs go missing, crossed, or unterminated, so a stray edit can't corrupt a block or make the generator silently no-op. |
| `requirements.txt` | `pyyaml` + `python-frontmatter`, the only dependencies. |

## What feeds what

Each block is a projection of one source of truth on the site:

| Block | Source (in `zaherkarp/zaherkarp.github.io`) |
| --- | --- |
| Title | `src/content/resume.md`, the current ("Present") role |
| Stack | `src/content/skills.yaml` (categories + skills) |
| Writing | `src/content/blog/*.md` frontmatter (recent non-draft posts) |
| Research | `src/content/publications.yaml` (count + most-cited) |

## Running it by hand

The sync runs on its own (see Automation). To run it locally, clone the public
site somewhere and point the generator at it:

```bash
git clone --depth 1 https://github.com/zaherkarp/zaherkarp.github.io site
pip install -r scripts/requirements.txt
python scripts/build_readme.py --site site
python scripts/lint_markers.py
```

Re-running with unchanged inputs leaves `README.md` byte-identical.

## Automation

`.github/workflows/sync-readme.yml` runs daily, plus a manual **Run workflow**
button. It clones the public site, regenerates the blocks, and commits only if
something changed, using the built-in `GITHUB_TOKEN`. **No secrets:** the read
side is a public repo and the write side commits to this one. A companion
`.github/workflows/lint.yml` runs `lint_markers.py` on every pull request and
push.

## Do not hand-edit the generated blocks

Anything between the four marker pairs in `README.md` is overwritten on the next
sync. Change the content at its source on the site instead. Because the
generator reads the site's field names (`skills.yaml` keys, `publications.yaml`
fields, the resume's `**Employer** | Title` + "Present" shape), a schema rename
on the site needs a matching edit to `build_readme.py` here. That contract is
documented on the site in `CLAUDE.md` under "GitHub profile README (external
consumer)", and in its `docs/pipelines.md` (pipeline 10).
