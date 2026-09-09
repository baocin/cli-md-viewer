# <Feature title>

| Field | Value |
|---|---|
| Status | planned |
| Owner | <name or handle> (<agent or tool, e.g. Claude Code, Cursor, Codex, human>) |
| Branch | `<type>/<this-file-name-without-md>` |
| PR | <link, or blank> |
| Created | YYYY-MM-DD |
| Updated | YYYY-MM-DD |

## Goal

One paragraph. The reader-visible outcome, not the implementation.

## Scope

- What this feature includes.

## Out of scope

- What it deliberately does not include. Split these into other feature files if needed.

## Plan

- [ ] Step one
- [ ] Step two
- [ ] Docs updated (README.md / CONTRIBUTING.md / AGENTS.md) if a contract, parameter, key or binding changed
- [ ] CHANGELOG.md line under Unreleased
- [ ] DECISIONS.md entries for any choice that reaches beyond this feature (cite as D-nnn below)

## Verification

Fill in before status moves to `review`.

| Check | Result |
|---|---|
| `PYTHONPATH=src python3 tests/test_render.py` | n/n |
| `mdv samples/kitchen-sink.md -w 80` looked at | |
| Documents rendered by eye (which ones) | |

## Decisions

- Choices a future reader would otherwise re-litigate, with the reason.

## Progress log

Newest entry last. One entry per working session.

- YYYY-MM-DD <owner>: created.
