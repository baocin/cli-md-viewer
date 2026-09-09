# Contributing

## Setup

```sh
git clone git@github.com:baocin/cli-md-viewer.git
cd cli-md-viewer
pip install -e .
PYTHONPATH=src python3 tests/test_render.py
```

## The loop

1. Create `work/<feature>.md` from `work/_template.md` and register it in `work/todo.md`.
2. Branch `<type>/<feature>`.
3. Change `src/mdv/render.py` (rendering) or `src/mdv/cli.py` (flags and I/O).
4. Add a construct to `samples/kitchen-sink.md` and a test to `tests/test_render.py`.
5. Run the suite, then **look at** `mdv samples/kitchen-sink.md -w 80`. A passing suite
   with ugly output is a failure; the whole point of the project is what it looks like.
6. Add a `CHANGELOG.md` line under Unreleased, and a `DECISIONS.md` entry for anything a
   future reader would otherwise re-litigate.
7. Open a PR linking the feature file.

## Adding support for a construct

Rendering dispatches on node type: a block node of type `foo` is handled by
`_Renderer._b_foo`, inline nodes in `_Renderer._inline`. To add one:

- Enable the parser plugin in `parser()`.
- Add the handler(s).
- Add colours to `STYLES`, never inline in the handler.
- Add the construct to `samples/kitchen-sink.md`.
- Add a test asserting on the plain-text render.

## Style

- Standard library and the three existing dependencies. A fourth needs a `DECISIONS.md`
  entry arguing for it.
- No config file, no themes system, no plugin API until something concrete needs one.
- Comments explain why, not what.
