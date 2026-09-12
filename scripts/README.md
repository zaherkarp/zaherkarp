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
