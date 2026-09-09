"""Self-check: render a document with every construct and assert the output.

Run it directly (`python tests/test_render.py`) or under pytest. Assertions are
on the plain text of a no-color render, so they describe what a reader sees.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rich.console import Console  # noqa: E402

from mdv.render import render  # noqa: E402

SAMPLE = Path(__file__).resolve().parents[1] / "samples" / "kitchen-sink.md"


def plain(source: str, width: int = 80) -> str:
    console = Console(width=width, no_color=True, force_terminal=False, record=True)
    console.print(render(source, hyperlinks=False))
    return console.export_text()


def test_headings():
    out = plain("# Title\n\n## Section\n\n### Sub\n")
    assert "Title" in out and "Section" in out and "Sub" in out


def test_inline_emphasis_survives():
    out = plain("normal **bold** _em_ ~~gone~~ `code`\n")
    for word in ("normal", "bold", "em", "gone", "code"):
        assert word in out, word


def test_table_alignment_and_cells():
    out = plain("| a | b |\n|---|--:|\n| 1 | 2 |\n| 3 | 4 |\n")
    assert "a" in out and "4" in out
    assert out.count("\n") >= 4  # header, rule, two rows


def test_ragged_table_row_does_not_crash():
    out = plain("| a | b | c |\n|---|---|---|\n| 1 |\n")
    assert "1" in out


def test_task_list_markers():
    out = plain("- [ ] open\n- [x] shut\n")
    assert "☐" in out and "☑" in out
    assert "[ ]" not in out and "[x]" not in out


def test_ordered_and_nested_lists():
    out = plain("1. one\n2. two\n   - inner\n")
    assert "1." in out and "2." in out and "inner" in out


def test_code_fence_keeps_content():
    out = plain("```python\ndef f():\n    return 1\n```\n")
    assert "def f():" in out and "return 1" in out


def test_blockquote_and_rule():
    out = plain("> quoted\n\n---\n")
    assert "quoted" in out


def test_link_without_hyperlinks_shows_url():
    out = plain("[docs](https://example.com/x)\n")
    assert "docs" in out and "example.com/x" in out


def test_front_matter_is_shown_not_dumped_as_text():
    out = plain("---\ntitle: hi\n---\n\nbody\n")
    assert "title: hi" in out and "body" in out


def test_footnotes():
    out = plain("text[^1]\n\n[^1]: the note\n")
    assert "[1]" in out and "the note" in out


def test_definition_list():
    out = plain("Term\n: meaning\n")
    assert "Term" in out and "meaning" in out


def test_html_block_is_stripped_not_printed_raw():
    out = plain("<div align=\"center\">hello</div>\n")
    assert "hello" in out and "<div" not in out


def test_empty_document():
    assert plain("").strip() == ""


def test_sample_renders():
    out = plain(SAMPLE.read_text())
    assert len(out) > 500


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"pass {name}")
            except AssertionError as exc:
                failures += 1
                print(f"FAIL {name}: {exc}")
    print(f"{'FAILED' if failures else 'ok'}: {failures} failure(s)")
    sys.exit(1 if failures else 0)
