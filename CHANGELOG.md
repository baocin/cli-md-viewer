# Changelog

Newest first. Every PR adds its line under Unreleased; a release moves them into a dated
section.

## Unreleased

- Initial renderer: headings, emphasis, strikethrough, inline code, links (OSC 8), images,
  bullet and ordered lists with nesting and tight/loose spacing, task lists, GFM tables
  with per-column alignment, fenced and indented code with syntax highlighting,
  blockquotes, thematic breaks, footnotes, definition lists, YAML front matter, and text
  extraction from raw HTML.
- `mdv` CLI: file or stdin, `--width`, `--pager`, `--no-color`, `--no-hyperlinks`.
- `tests/test_render.py`: 15 checks over the plain-text render, runnable without pytest.
- `samples/kitchen-sink.md`: every supported construct in one file.
- Declare `markdown-it-py[linkify]`: a clean-environment install crashed on any document
  because the linkify rule needs `linkify-it-py` (D-008).
- Project docs: `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `DECISIONS.md` (D-001 to
  D-007) and the `work/` feature-file workflow.
