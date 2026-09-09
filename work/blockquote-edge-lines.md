# Blockquote edge lines

| Field | Value |
|---|---|
| Status | planned |
| Owner | unassigned |
| Branch | `fix/blockquote-edge-lines` |
| PR | |
| Created | 2026-09-08 |
| Updated | 2026-09-08 |

## Goal

A blockquote's bar covers exactly the quoted lines. Today it draws one extra bar segment
above the first line and one below the last, because the bar is a Rich `Panel` with a
custom box and a panel always emits its top and bottom rows.

## Scope

- Bar starts on the first line of quoted content and ends on the last.
- Nesting keeps working; two levels already draw two bars.

## Out of scope

- Changing the bar character or colour.

## Plan

- [ ] Reproduce: `printf '> a\n' | mdv --no-color -`, three bar lines for one line of text
- [ ] Either give `Panel` zero-height edges or build the bar by rendering the inner group
      to lines and prefixing each
- [ ] Test asserting bar-line count equals content-line count
- [ ] CHANGELOG line

## Verification

| Check | Result |
|---|---|
| `PYTHONPATH=src python3 tests/test_render.py` | n/n |
| `mdv samples/kitchen-sink.md -w 80` looked at | |
| Documents rendered by eye (which ones) | |

## Decisions

- Supersedes nothing; D-006 chose the bar, this is its remaining defect.

## Progress log

- 2026-09-08 Michael Pedersen (Claude Code): filed while building the initial renderer.
  Checked nesting at the same time: two-level quotes already render two bars, so only the
  edge lines are wrong.
