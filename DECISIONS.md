# Decisions

Numbered, newest last. A decision that reaches beyond one feature gets an entry here in
the same PR that makes it. Superseding an entry means writing a new one that says so, not
editing the old one.

## D-001: markdown-it-py for parsing, not rich.markdown

`rich.markdown.Markdown` exists and is one line to use. It was rejected after rendering
`work/todo.md` from another project with it: strikethrough vanished, task list boxes came
out as literal `[ ]`, definition lists rendered as `Term : def` on one line, and there is
no hook to fix any of it short of subclassing internals.

markdown-it-py gives a full token tree with plugins for the GFM extensions, and Rich is
kept for what it is genuinely good at: laying out and styling renderables. The renderer is
ours, which is the point of the project.

## D-002: three dependencies, no more

`rich`, `markdown-it-py`, `mdit-py-plugins`. A fourth dependency needs an entry here
arguing why the standard library and these three cannot do it. Pygments arrives
transitively through Rich and is used for fence highlighting; that is not a fourth.

## D-003: no config file, no theme system

Colours live in `STYLES` in `render.py`. A theme system is speculative until someone asks
for a second theme; `--no-color` covers the case that actually comes up, which is piping
the output somewhere. Revisit if a light-terminal user reports the palette is unreadable.

## D-004: unknown constructs fall back to text, never to raw markdown

`_Renderer.block` renders children, or the node's text content, for any type without a
handler. The alternative, printing the source, is exactly the failure the project exists
to fix, so it is a bug by definition. Documented as hard rule 2 in `AGENTS.md`.

## D-005: OSC 8 hyperlinks by default

Links are terminal hyperlinks, with the URL hidden. Terminals that do not support OSC 8
show the text and drop the escape, which is still readable, and `--no-hyperlinks` prints
`text (url)` for the case where the URL itself matters.

## D-006: blockquote is a left bar, not a panel

The first implementation boxed quotes in a heavy panel. At a width of 80 that is louder
than the quote itself. A left bar drawn on every wrapped line, via a custom Rich box, reads
as a quote without competing with headings for attention.

## D-007: the test suite runs without pytest

`tests/test_render.py` has a `__main__` block that runs every `test_*` function and exits
non-zero on failure, so the suite works with nothing installed but the dependencies. It is
still a valid pytest module for anyone who wants that.
