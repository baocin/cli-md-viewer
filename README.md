# mdv

A terminal markdown viewer that renders what the document says.

Piping a README through `cat` gives you raw pipes, hashes and backticks. `mdv` gives you
the table, the heading and the checkbox.

```sh
mdv README.md
mdv work/todo.md -p          # through a pager
cat notes.md | mdv           # stdin
mdv doc.md -w 100            # fixed width
```

## Install

```sh
pipx install -e .            # or: pip install -e .
```

Python 3.10+. Dependencies: `rich`, `markdown-it-py`, `mdit-py-plugins`.

Without installing:

```sh
PYTHONPATH=src python3 -m mdv FILE.md
```

## What it renders

CommonMark plus GitHub flavour plus the extensions people actually put in documents:

| Construct | Rendering |
|---|---|
| Headings | H1 boxed, H2 underruled, H3-H6 coloured by level |
| Emphasis | bold, italic, ~~strikethrough~~, `inline code` on a background |
| Links | OSC 8 terminal hyperlinks, or `text (url)` with `--no-hyperlinks` |
| Images | `🖼 alt` linked to the source |
| Lists | bullets by nesting depth, aligned ordinals, tight and loose spacing |
| Task lists | `☐` and `☑` |
| Tables | column alignment from the delimiter row, wrapped cells |
| Code fences | syntax highlighting by info string |
| Blockquotes | left bar on every wrapped line, nesting preserved |
| Footnotes | reference marks inline, notes in a block at the end |
| Definition lists | bold term, indented definition |
| Front matter | YAML shown in its own panel, not dumped as text |
| Raw HTML | reduced to its text content |

`samples/kitchen-sink.md` contains all of it. Render that file to see the whole surface:

```sh
mdv samples/kitchen-sink.md
```

## Options

```
mdv [file] [-w WIDTH] [-p] [--no-color] [--no-hyperlinks]
```

| Flag | Effect |
|---|---|
| `file` | markdown file, or `-`/omitted for stdin |
| `-w`, `--width` | wrap width; default is the terminal capped at 100 columns |
| `-p`, `--pager` | page the output, styles preserved |
| `--no-color` | plain text, for piping to a file or a diff |
| `--no-hyperlinks` | print URLs instead of OSC 8 escapes |

## Tests

```sh
PYTHONPATH=src python3 tests/test_render.py
```

No pytest required; it also runs under pytest if you prefer.

## Contributing

Read [AGENTS.md](AGENTS.md). Every change starts as a feature file in `work/`.
