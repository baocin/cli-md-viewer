# AGENTS.md

Source of truth for every coding agent working in this repository, whatever model or
harness runs it. `CLAUDE.md` and any other tool-specific file only point here. Humans
should read [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md) as well.

## Before you start

1. Read this file end to end.
2. Read `DECISIONS.md`. It records why the project is the way it is. Anything that looks
   odd probably has an entry; find it before you change it.
3. Skim `CHANGELOG.md` from the top so you know what has shipped.
4. Read `work/todo.md` to see what is in flight and who owns it.
5. Find or create the feature file for your task under `work/` (see "Work flow").
   No code changes without a feature file.

## What this is

`mdv` renders a markdown file in a terminal the way the document actually reads:
headings, tables, code, task lists, footnotes, definition lists and front matter all
render as themselves, not as raw punctuation. Python 3.10+, three dependencies
(`rich`, `markdown-it-py`, `mdit-py-plugins`), no framework, no config file.

The bar the project is judged against: **anything valid in the document renders as
something a reader recognises.** An unhandled construct falling back to raw markdown is
a bug, not a limitation.

## Commands

```sh
pipx install -e .                       # or: pip install -e .
mdv FILE.md                             # render
mdv FILE.md -p                          # page it
cat FILE.md | mdv                        # stdin
mdv samples/kitchen-sink.md -w 80        # fixed width, the eyeball test
PYTHONPATH=src python3 tests/test_render.py   # the suite, no pytest needed
PYTHONPATH=src python3 -m mdv FILE.md    # run without installing
```

`tests/test_render.py` runs standalone or under pytest. It must pass before any commit.

## Layout

| Path | Role |
|---|---|
| `src/mdv/render.py` | Parser setup and the whole token-tree to Rich renderer. All rendering decisions live here. |
| `src/mdv/cli.py` | Argument parsing, input selection, console and pager. No rendering logic. |
| `src/mdv/__main__.py` | `python -m mdv` entry. |
| `tests/test_render.py` | Assertions on the plain-text render. One test per construct. |
| `samples/kitchen-sink.md` | Every supported construct in one file. The visual regression check. |
| `work/` | Feature files; see "Work flow". |

## Hard rules

1. **Every construct the parser emits has a handler.** `_Renderer.block` dispatches on
   `_b_<node type>`. Adding a parser plugin means adding its handlers in the same change.
2. **The fallback never prints raw markdown.** Unknown block: render children, else the
   node's text content. A user must never see `##` or `|---|` in the output.
3. **Styles live in `STYLES`.** No colour literals scattered through the renderer.
4. **Rendering is pure.** `render(source) -> RenderableType`. No printing, no file access,
   no `sys.stdout` inside `render.py`; the CLI owns the console.
5. **New dependencies need a `DECISIONS.md` entry.** Three is the budget; a fourth must
   earn its place in writing.
6. **Every new construct gets a test and a line in `samples/kitchen-sink.md`.** The test
   asserts on `--no-color` plain text, which is what a reader sees.
7. **Degrade, do not crash.** Ragged tables, unclosed fences, stray HTML, empty files:
   render something. `tests/test_render.py` has cases for each; keep adding them.

## Work flow

All work is tracked as markdown feature files under `work/`.

```
work/
  todo.md            index of every feature, active and complete, with status
  <feature>.md       one file per active feature
  _template.md       copy this to start a feature
  complete/          finished feature files, moved here verbatim
```

### Rules

1. **One feature, one file.** Before writing code, create `work/<feature>.md` from
   `work/_template.md`, named in kebab-case after the outcome. If a file for the feature
   exists, work in that one.
2. **Register it.** Add a row to the Active table in `work/todo.md` in the same commit
   that creates the feature file.
3. **Claim it.** Owner field gets your name or handle and the tool you are using.
4. **Keep it current.** Every session ends with a progress log entry and an updated
   Status. The status in `todo.md` must match the status in the feature file.
5. **Statuses** are exactly one of: `planned`, `in-progress`, `blocked`, `review`, `done`.
   `blocked` requires a line saying what unblocks it.
6. **Done means verified.** The suite has been run with its pass count recorded and the
   rendered output has been looked at, not just diffed.
7. **Move it.** On `done`, `git mv work/<feature>.md work/complete/<feature>.md` and move
   its row to the Complete table in `todo.md`, in the same commit.
8. **Scope changes are new features.** Update Goal and Scope with a log entry, or split
   the extra work into its own file.
9. **Never delete a feature file.** Cancelled work gets status `done` with a log entry
   saying it was dropped and why, then moves to `complete/`.
10. **Docs travel with the change.** A new flag, construct or rule updates `README.md`,
    `CONTRIBUTING.md` or this file inside the same feature.
11. **Records travel with the change.** Every PR adds a line to `CHANGELOG.md` under
    Unreleased, and copies any decision reaching beyond the feature into `DECISIONS.md`
    as a new numbered entry.
12. **Plans live in the feature file.** If a tool insists on its own plan document, copy
    the plan into the feature file before the first code change.

### Agents specifically

- At the start of a session read `DECISIONS.md`, `work/todo.md` and your feature file
  before reading code. At the end, write the log entry before reporting to the user.
- Before changing something because it looks wrong, search `DECISIONS.md` for it. Follow
  the entry or write a superseding one and say so. Never silently undo a decision.
- Report status in the user's terms: pass counts, what you looked at, what remains.
- Do not mark `done`, move files to `complete/` or merge without the user asking.
- A rendering bug you find outside your feature becomes a `planned` feature file with the
  offending markdown pasted in, unless the user says to fix it now.

## Git conventions

- Branch `<type>/<feature-file-name>`, types `feat`, `fix`, `art`, `docs`, `chore`.
- Commit subject `<type>(<area>): <what changed>`, imperative, lower case.
- One PR per feature file, linking it. The last commit before merge is the one that moves
  the file to `complete/`.
- `main` always renders `samples/kitchen-sink.md` without a traceback.
