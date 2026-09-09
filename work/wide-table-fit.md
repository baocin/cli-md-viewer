# Wide table fit

| Field | Value |
|---|---|
| Status | planned |
| Owner | unassigned |
| Branch | `fix/wide-table-fit` |
| PR | |
| Created | 2026-09-08 |
| Updated | 2026-09-08 |

## Goal

A table with five or more columns stays readable at 80 to 100 columns instead of
squeezing every cell into a four-character ribbon of wrapped words.

## Scope

- A fit strategy for tables wider than the console: candidates are dropping to a
  record-per-row layout below a threshold, letting the table overflow with horizontal
  truncation, or weighting column widths by content length instead of Rich's default.
- The choice gets a `DECISIONS.md` entry; it changes how a whole class of document looks.

## Out of scope

- Interactive horizontal scrolling.

## Plan

- [ ] Reproduce with KESSEL `work/todo.md` at width 80, 100 and 200
- [ ] Try the candidate strategies, look at each
- [ ] Implement the winner, `DECISIONS.md` entry
- [ ] Test asserting every cell's text survives at width 60
- [ ] CHANGELOG line

## Verification

| Check | Result |
|---|---|
| `PYTHONPATH=src python3 tests/test_render.py` | n/n |
| `mdv samples/kitchen-sink.md -w 80` looked at | |
| Documents rendered by eye (which ones) | |

## Decisions

- To be recorded with the chosen strategy.

## Progress log

- 2026-09-08 Michael Pedersen (Claude Code): filed while building the initial renderer.
  The five-column Active table in KESSEL's `work/todo.md` is the reproduction: at width 80
  the Notes column wraps to two words per line.
