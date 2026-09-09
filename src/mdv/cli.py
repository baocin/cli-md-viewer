"""Command line entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console

from .render import render


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="mdv",
        description="Render a markdown file in the terminal.",
    )
    ap.add_argument("file", nargs="?", help="markdown file, or - for stdin (default)")
    ap.add_argument("-w", "--width", type=int, default=None, help="wrap width (default: terminal, capped at 100)")
    ap.add_argument("-p", "--pager", action="store_true", help="page the output")
    ap.add_argument("--no-color", action="store_true", help="plain text, no styling")
    ap.add_argument("--no-hyperlinks", action="store_true", help="print URLs instead of OSC 8 links")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.file in (None, "-"):
        if sys.stdin.isatty():
            build_parser().print_help()
            return 2
        source = sys.stdin.read()
    else:
        path = Path(args.file)
        if not path.is_file():
            print(f"mdv: {path}: no such file", file=sys.stderr)
            return 1
        source = path.read_text(encoding="utf-8", errors="replace")

    console = Console(
        width=args.width or min(Console().width, 100),
        no_color=args.no_color,
        force_terminal=None if args.no_color else True,
    )
    doc = render(source, hyperlinks=not args.no_hyperlinks)
    if args.pager:
        with console.pager(styles=not args.no_color):
            console.print(doc)
    else:
        console.print(doc)
    return 0
