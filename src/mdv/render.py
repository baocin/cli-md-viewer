"""Markdown token tree -> Rich renderables.

The parser is markdown-it-py in its `gfm-like` preset plus the plugins for the
extensions people actually put in READMEs: task lists, definition lists,
footnotes and YAML front matter. Every node type the parser can emit has a
handler here; anything unknown falls back to its plain text so a document never
renders as an empty block.
"""

from __future__ import annotations

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from rich.align import Align
from rich.console import Group, RenderableType
from rich.padding import Padding
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table, box
from rich.text import Text

STYLES = {
    "h1": "bold #ffffff on #005f87",
    "h2": "bold #5fd7ff",
    "h3": "bold #87d7ff",
    "h4": "bold #afafff",
    "h5": "bold",
    "h6": "bold dim",
    "code": "bold #ffd787 on #262626",
    "link": "underline #5fafff",
    "quote": "italic #a8a8a8",
    "quote_bar": "#5f5f5f",
    "rule": "#5f5f5f",
    "bullet": "bold #5fd7ff",
    "task_done": "bold #5fd75f",
    "task_todo": "#8a8a8a",
    "table_header": "bold #5fd7ff",
    "table_border": "#5f5f5f",
    "frontmatter": "dim italic",
    "image": "italic #d787d7",
    "footnote_ref": "#d7af5f",
    "term": "bold",
}

QUOTE_BOX = box.Box("\u258c   \n" * 8)

BULLETS = ["•", "◦", "‣", "⁃"]

_ALIGN = {"left": "left", "center": "center", "right": "right", None: "left"}


def parser() -> MarkdownIt:
    md = MarkdownIt("gfm-like", {"linkify": True, "html": True})
    return (
        md.use(tasklists_plugin, enabled=True)
        .use(deflist_plugin)
        .use(footnote_plugin)
        .use(front_matter_plugin)
        .enable("table")
    )


def render(source: str, hyperlinks: bool = True) -> RenderableType:
    """Parse `source` and return one Rich renderable for the whole document."""
    tree = SyntaxTreeNode(parser().parse(source))
    return Group(*_Renderer(hyperlinks).blocks(tree.children))


class _Renderer:
    def __init__(self, hyperlinks: bool = True) -> None:
        self.hyperlinks = hyperlinks
        self.list_depth = 0

    # --- blocks -----------------------------------------------------------

    def blocks(self, nodes) -> list[RenderableType]:
        """Render sibling blocks, blank line between them.

        A tight list (markdown-it marks its paragraphs `hidden`) and a nested
        list under its parent item get no blank line, which is what the source
        looks like and what every other renderer does.
        """
        out: list[RenderableType] = []
        previous = None
        for node in nodes:
            item = self.block(node)
            if item is None:
                continue
            if out and not _tight(previous, node):
                out.append(Text(""))
            out.append(item)
            previous = node
        return out

    def block(self, node: SyntaxTreeNode) -> RenderableType | None:
        handler = getattr(self, f"_b_{node.type}", None)
        if handler is not None:
            return handler(node)
        if node.children:
            return Group(*self.blocks(node.children))
        text = (node.content or "").strip()
        return Text(text) if text else None

    def _b_paragraph(self, node) -> RenderableType:
        return self.inline(node.children[0])

    def _b_heading(self, node) -> RenderableType:
        level = int(node.tag[1])
        text = self.inline(node.children[0])
        text.stylize(STYLES[f"h{level}"])
        if level == 1:
            return Panel(Align.center(text), box=box.HEAVY, border_style=STYLES["h2"])
        if level == 2:
            return Group(text, Rule(style=STYLES["rule"], characters="─"))
        return text

    def _b_hr(self, node) -> RenderableType:
        return Rule(style=STYLES["rule"])

    def _b_fence(self, node) -> RenderableType:
        lang = (node.info or "").split()[0] if node.info else "text"
        return Syntax(
            node.content.rstrip("\n"),
            lang,
            theme="ansi_dark",
            background_color="#1c1c1c",
            word_wrap=True,
        )

    _b_code_block = _b_fence

    def _b_blockquote(self, node) -> RenderableType:
        return Panel(
            Group(*self.blocks(node.children)),
            box=QUOTE_BOX,
            border_style=STYLES["quote_bar"],
            padding=(0, 1),
            style=STYLES["quote"],
        )

    def _b_bullet_list(self, node) -> RenderableType:
        return self._list(node, ordered=False)

    def _b_ordered_list(self, node) -> RenderableType:
        return self._list(node, ordered=True)

    def _list(self, node, ordered: bool) -> RenderableType:
        start = int(node.attrs.get("start", 1)) if ordered else 1
        loose = any(
            child.type == "paragraph" and not child.hidden
            for item in node.children
            for child in item.children
        )
        marker_style = STYLES["bullet"]
        rows: list[RenderableType] = []
        self.list_depth += 1
        try:
            width = max(
                len(f"{start + i}.") for i in range(max(len(node.children), 1))
            ) if ordered else 1
            for i, item in enumerate(node.children):
                body = Group(*self.blocks(item.children))
                task = item.attrs.get("class", "")
                if "task-list-item" in str(task):
                    checked = _is_checked(item)
                    marker = Text(
                        "☑" if checked else "☐",
                        style=STYLES["task_done"] if checked else STYLES["task_todo"],
                    )
                elif ordered:
                    marker = Text(f"{start + i}.".rjust(width), style=marker_style)
                else:
                    marker = Text(
                        BULLETS[(self.list_depth - 1) % len(BULLETS)],
                        style=marker_style,
                    )
                grid = Table.grid(padding=(0, 1))
                grid.add_column(width=len(marker.plain), no_wrap=True)
                grid.add_column(overflow="fold")
                grid.add_row(marker, body)
                if rows and loose:
                    rows.insert(len(rows), Text(""))
                rows.append(grid)
        finally:
            self.list_depth -= 1
        return Padding(Group(*rows), (0, 0, 0, 2 if self.list_depth else 0))

    def _b_table(self, node) -> RenderableType:
        table = Table(
            box=box.SIMPLE_HEAD,
            border_style=STYLES["table_border"],
            header_style=STYLES["table_header"],
            expand=False,
            pad_edge=False,
        )
        head = [c for c in node.children if c.type == "thead"]
        body = [c for c in node.children if c.type == "tbody"]
        aligns: list[str] = []
        if head:
            for cell in head[0].children[0].children:
                aligns.append(_cell_align(cell))
                table.add_column(self.inline(cell.children[0]), justify=aligns[-1])
        for section in body:
            for row in section.children:
                cells = [self.inline(c.children[0]) if c.children else Text("") for c in row.children]
                while len(cells) < len(table.columns):
                    cells.append(Text(""))
                table.add_row(*cells[: len(table.columns) or len(cells)])
        return table

    def _b_dl(self, node) -> RenderableType:
        rows: list[RenderableType] = []
        for child in node.children:
            if child.type == "dt":
                text = self.inline(child.children[0])
                text.stylize(STYLES["term"])
                rows.append(text)
            elif child.type == "dd":
                rows.append(Padding(Group(*self.blocks(child.children)), (0, 0, 0, 4)))
        return Group(*rows)

    def _b_front_matter(self, node) -> RenderableType:
        return Panel(
            Syntax(node.content.strip(), "yaml", theme="ansi_dark", background_color="#1c1c1c"),
            title="front matter",
            title_align="left",
            box=box.ROUNDED,
            border_style=STYLES["rule"],
        )

    def _b_footnote_block(self, node) -> RenderableType:
        return Group(Rule(style=STYLES["rule"]), *self.blocks(node.children))

    def _b_footnote(self, node) -> RenderableType:
        label = Text(f"[{node.meta.get('label', node.attrs.get('id', ''))}]", style=STYLES["footnote_ref"])
        body = Group(*self.blocks([c for c in node.children if c.type != "footnote_anchor"]))
        grid = Table.grid(padding=(0, 1))
        grid.add_column(no_wrap=True)
        grid.add_column(overflow="fold")
        grid.add_row(label, body)
        return grid

    def _b_html_block(self, node) -> RenderableType | None:
        text = _strip_html(node.content).strip()
        return Text(text, style="dim") if text else None

    # --- inline -----------------------------------------------------------

    def inline(self, node: SyntaxTreeNode) -> Text:
        text = Text()
        for child in node.children:
            text.append_text(self._inline(child))
        return text

    def _inline(self, node: SyntaxTreeNode) -> Text:
        t = node.type
        if t == "text":
            return Text(node.content)
        if t == "code_inline":
            return Text(f" {node.content} ", style=STYLES["code"])
        if t == "softbreak":
            return Text(" ")
        if t == "hardbreak":
            return Text("\n")
        if t in ("strong", "em", "s"):
            inner = self._children(node)
            inner.stylize({"strong": "bold", "em": "italic", "s": "strike"}[t])
            return inner
        if t == "link":
            inner = self._children(node)
            href = node.attrs.get("href", "")
            inner.stylize(STYLES["link"])
            if self.hyperlinks and href:
                inner.stylize(f"link {href}")
            elif href and inner.plain != href:
                inner.append(f" ({href})", style="dim")
            return inner
        if t == "image":
            alt = self._children(node).plain or node.attrs.get("alt", "") or "image"
            src = node.attrs.get("src", "")
            out = Text(f"\U0001f5bc {alt}", style=STYLES["image"])
            if self.hyperlinks and src:
                out.stylize(f"link {src}")
            elif src:
                out.append(f" ({src})", style="dim")
            return out
        if t == "footnote_ref":
            label = node.meta.get("label", node.meta.get("id", ""))
            return Text(f"[{label}]", style=STYLES["footnote_ref"])
        if t == "html_inline":
            return Text(_strip_html(node.content))
        if t == "checkbox_input":  # handled by the list marker
            return Text()
        if node.children:
            return self._children(node)
        return Text(node.content or "")

    def _children(self, node: SyntaxTreeNode) -> Text:
        text = Text()
        for child in node.children:
            text.append_text(self._inline(child))
        return text


def _tight(previous, node) -> bool:
    if previous is None:
        return False
    if node.type in ("bullet_list", "ordered_list") and getattr(previous, "hidden", False):
        return True
    return bool(getattr(previous, "hidden", False) and getattr(node, "hidden", False))


def _is_checked(item: SyntaxTreeNode) -> bool:
    for node in item.walk():
        if node.type == "checkbox_input":
            return bool(node.attrs.get("checked", False))
        if node.type == "html_inline" and "checked" in node.content:
            return True
    return False


def _cell_align(cell: SyntaxTreeNode) -> str:
    style = str(cell.attrs.get("style", ""))
    for name in ("center", "right", "left"):
        if name in style:
            return name
    return "left"


def _strip_html(raw: str) -> str:
    out, depth = [], 0
    for ch in raw:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(ch)
    return "".join(out)
