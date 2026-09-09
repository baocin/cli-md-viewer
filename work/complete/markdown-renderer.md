# Markdown renderer and mdv CLI

| Field | Value |
|---|---|
| Status | done |
| Owner | Michael Pedersen (Claude Code) |
| Branch | `main` |
| PR | initial commit |
| Created | 2026-09-08 |
| Updated | 2026-09-08 |

## Goal

Reading a markdown file in a terminal shows the document, not its source. Headings, tables,
task lists, footnotes and front matter each render as themselves, at any terminal width,
for any markdown a real README or work log contains.

## Scope

- Parser: CommonMark plus GFM (tables, strikethrough, autolinks) plus task lists,
  definition lists, footnotes and YAML front matter.
- Renderer from the markdown-it token tree to Rich renderables, one handler per node type.
- `mdv` CLI: file or stdin, width, pager, `--no-color`, `--no-hyperlinks`.
- `samples/kitchen-sink.md` and a standalone test suite.
- Project documentation and the `work/` workflow.

## Out of scope

- Themes and configuration (D-003).
- Terminal image protocols for images; alt text and a link only.
- Editing, scrolling UI, or file watching.

## Plan

- [x] Compare `rich.markdown` against a real document, record the result (D-001)
- [x] Parser setup with plugins
- [x] Block handlers: heading, paragraph, lists, table, code, quote, hr, dl, footnotes,
      front matter, html
- [x] Inline handlers: emphasis, strikethrough, code, links, images, breaks, footnote refs
- [x] CLI and packaging
- [x] Sample document and test suite
- [x] Docs: README, AGENTS, CONTRIBUTING, DECISIONS, CHANGELOG

## Verification

| Check | Result |
|---|---|
| `PYTHONPATH=src python3 tests/test_render.py` | 15/15 |
| `mdv samples/kitchen-sink.md -w 80` looked at | yes |
| Documents rendered by eye | `samples/kitchen-sink.md`, KESSEL `work/todo.md` (the document that prompted the project), this repo's `README.md` and `AGENTS.md` |

## Decisions

- D-001 markdown-it-py over `rich.markdown`
- D-002 three dependencies
- D-003 no config or theme system
- D-004 unknown constructs fall back to text
- D-005 OSC 8 hyperlinks by default
- D-006 blockquote as a left bar
- D-007 suite runs without pytest

## Progress log

- 2026-09-08 Michael Pedersen (Claude Code): created. Rendered KESSEL's `work/todo.md`
  with `rich.markdown` first: strikethrough dropped, task boxes literal, definition list
  collapsed to one line. Built the token-tree renderer instead. Two visual bugs found by
  looking at the output rather than by the suite: a heavy panel around blockquotes (now a
  left bar, D-006) and blank lines inside tight lists (now suppressed when markdown-it
  marks the item paragraphs hidden). Suite 15/15. Left two known limitations as feature
  files: wide-table-fit and nested-blockquote-depth.
