---
title: Kitchen sink
tags: [markdown, terminal]
---

# Kitchen sink

Every construct `mdv` claims to render, in one file. Use it to eyeball a change:
`mdv samples/kitchen-sink.md`.

## Inline

Plain text with **bold**, _italic_, ***both***, ~~struck~~, `inline code`, a
[link](https://example.com/docs), an autolink https://example.com, and a
footnote reference[^why].

[^why]: Footnotes render in a block at the end, numbered as written.

## Lists

- Bullet
- Bullet with a long line that wraps past the width of a narrow terminal to show
  how continuation lines line up under the text and not under the marker
  - Nested bullet
    - Third level

1. First
2. Second
10. Tenth, to check marker alignment

- [x] Finished task
- [ ] Unfinished task

## Table

| Left | Centre | Right |
|:-----|:------:|------:|
| a | b | 1 |
| longer cell | mid | 20 |
| `code` | **bold** | 300 |

## Code

```python
def parse(source: str) -> str:
    """Fenced code keeps its highlighting."""
    return source.strip()
```

    indented code block

## Quote

> A blockquote, which may contain **inline styling** and
>
> - a list
> - of things

## Definitions

Parsec
: The unit KESSEL scores in. Lower is better.

## Rule

---

<div align="center">Raw HTML is reduced to its text.</div>
