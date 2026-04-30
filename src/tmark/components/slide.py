from typing import ClassVar, override

from rich.align import Align
from rich.columns import Columns
from rich.console import RenderableType
from rich.style import Style
from rich.table import Table
from rich.text import Text
from sympy.parsing.latex import parse_latex
from sympy.printing import pretty
from textual import highlight
from textual.app import ComposeResult, RenderResult
from textual.widget import Widget
from textual.widgets import Static
from textual_image.renderable import Image

from tmark.token import MistuneToken


# Markdown block
class MarkdownBlock(Widget):
    """
    Base class for markdown block items.
    This class does not render or compose anything - so it is not recommended to use this
    as a standalone widget.
    This class just provides common utilities and styling.
    """

    token: MistuneToken

    # CSS
    DEFAULT_CSS: ClassVar[str] = """
    MarkdownBlock {
      height: auto;
    }
    """

    # __init__
    def __init__(
        self,
        token: MistuneToken,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        markup: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            markup=markup,
        )

        self.token = token


# Markdown container block
class MarkdownContainerBlock(MarkdownBlock):
    """Markdown block containing block children"""

    # CSS
    DEFAULT_CSS: ClassVar[str] = """
    MarkdownContainerBlock {
      layout: grid;
      grid-size: 1;
      grid-gutter: 1;
      grid-rows: auto;
    }
    """

    # compose
    @override
    def compose(self) -> ComposeResult:
        for block in self.token.children:
            match block.type:
                case "heading":
                    yield MarkdownHeading(block)

                case "paragraph":
                    yield MarkdownParagraph(block)

                case "block_code":
                    yield MarkdownBlockCode(block)

                case "block_quote":
                    yield MarkdownBlockquote(block)

                case "list":
                    yield MarkdownList(block)

                case "block_text":
                    yield MarkdownBlockText(block)

                case "table":
                    yield MarkdownTable(block)

                case "block_math":
                    yield MarkdownMath(block)

                case _:
                    continue


# Markdown leaf block
class MarkdownLeafBlock(MarkdownBlock):
    """Markdown block containing inline children"""

    # Component classes
    COMPONENT_CLASSES: ClassVar[set[str]] = {
        "markdown--codespan",
        "markdown--strong",
        "markdown--emphasis",
        "markdown--strikethrough",
        "markdown--link",
    }

    # CSS
    DEFAULT_CSS: ClassVar[str] = """
    MarkdownLeafBlock {
      & > .markdown--codespan {
        color: $text-primary 95%;
        background: $primary 10%;
      }

      & > .markdown--strong {
        text-style: bold;
      }

      & > .markdown--emphasis {
        text-style: italic;
      }

      & > .markdown--strikethrough {
        text-style: strike;
      }

      & > .markdown--link {
        color: $text-primary;
        text-style: underline;
      }
    }
    """

    # render
    @override
    def render(self) -> RenderResult:
        return self.render_inlines(self.token.children)

    # render_inlines
    def render_inlines(
        self,
        inlines: list[MistuneToken],
        style: Style = Style(),  # pyright: ignore[reportCallInDefaultInitializer]
    ) -> RenderableType:
        accumulator = Text()
        result = Table.grid(expand=False)

        # _accumulate
        def _accumulate(inline: MistuneToken, style: Style):
            nonlocal accumulator

            # Automatically update style with the inline specific style
            if (class_ := f"markdown--{inline.type}") in self.COMPONENT_CLASSES:
                style += self.get_component_rich_style(class_)

            # Link requires custom style applied
            if inline.type == "link":
                style += Style.from_meta(
                    {"@click": f"link('{inline.attrs.get('url')}')"}
                )

            # Match
            match inline.type:
                # text and codespan contain their content inside raw
                case "text" | "codespan":
                    accumulator = accumulator.append(inline.raw, style)

                # strong, emphasis and strikethrough contains inline children
                case "strong" | "emphasis" | "strikethrough" | "link":
                    for child in inline.children:
                        _accumulate(child, style)

                # linebreak
                case "linebreak":
                    accumulator = accumulator.append("\n", style)

                # softbreak
                case "softbreak":
                    accumulator = accumulator.append(" ", style)

                # image
                case "image":
                    # Since we cannot really flow an image and text together in a paragraph,
                    # What we do instead is push the accumulated text, then the image
                    # And start fresh with an empty accumulator from next line
                    if accumulator:
                        result.add_row(accumulator)

                    # Add image
                    result.add_row(Image(inline.attrs.get("url")))  # pyright: ignore[reportArgumentType]

                    # Clear accumulator
                    accumulator = Text()

                # inline_math
                case "inline_math":
                    accumulator = accumulator.append(inline.raw, style)

                case _:
                    return

        # For every inline
        for inline in inlines:
            _accumulate(inline, style)

        # Append the final accumulated text into result
        if accumulator:
            result.add_row(accumulator)

        # Return
        return result

    # action_link
    def action_link(self, url: str):
        self.app.open_url(url)  # pyright: ignore[reportUnknownMemberType]


# Markdown root
class MarkdownRoot(MarkdownContainerBlock):
    """Markdown root"""


# Markdown heading
class MarkdownHeading(MarkdownLeafBlock):
    """Markdown heading"""

    # Prefixes
    PREFIXES: list[str] = ["██", "███", "████", "░░░░░", "░░░░░░", "░░░░░░░"]

    # CSS
    DEFAULT_CSS: ClassVar[str] = """
    MarkdownHeading {
      &.level-1 {
        color: $text-primary;
      }

      &.level-2 {
        color: $text-success;
      }

      &.level-3 {
        color: $text-error;
      }

      &.level-4 {
        color: $text;
      }

      &.level-5 {
        color: $text-muted;
      }

      &.level-6 {
        color: $text-disabled;
      }
    }
    """

    # __init__
    def __init__(
        self,
        token: MistuneToken,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        markup: bool = True,
    ) -> None:
        super().__init__(token, name, id, classes, disabled, markup)

        # Add level as the class
        _ = self.add_class(f"level-{token.attrs.get('level')}")

    # render
    @override
    def render(self) -> RenderResult:
        prefix = self.render_prefix(self.token.attrs.get("level"))  # pyright: ignore[reportArgumentType]
        content = self.render_inlines(self.token.children)

        # Return
        return Columns([prefix, content])

    # render_prefix
    def render_prefix(self, level: int):
        return self.PREFIXES[level - 1]


# Markdown paragraph
class MarkdownParagraph(MarkdownLeafBlock):
    """Markdown paragraph"""


# Markdown block code
class MarkdownBlockCode(MarkdownLeafBlock):
    """Markdown block code"""

    # CSS
    DEFAULT_CSS: ClassVar[str] = """
    MarkdownBlockCode {
      padding: 1 2;
      background: $boost;
    }
    """

    # render
    @override
    def render(self) -> RenderResult:
        match self.token.style or "fenced":
            case "fenced":
                return highlight.highlight(self.token.raw)

            case "indent":
                return self.token.raw

            case _:
                raise Exception


# Markdown blockquote
class MarkdownBlockquote(MarkdownContainerBlock):
    """Markdown blockquote"""

    # CSS
    DEFAULT_CSS: ClassVar[str] = """
    MarkdownBlockquote {
      padding: 1 2;
      background: $boost;
      border-left: block $text-primary;
    }
    """


# Markdown list item
class MarkdownListItem(MarkdownContainerBlock):
    """Markdown list item"""

    bullet: str
    checked: bool | None

    # CSS
    DEFAULT_CSS: ClassVar[str] = """
    MarkdownListItem {
      layout: grid;
      grid-size: 2 1;
      grid-columns: auto 100%;

      .item-checked {
        color: $text-success 90%;
      }

      .item-unchecked {
        color: $surface;
      }
    }
    """

    # __init__
    def __init__(
        self,
        bullet: str,
        checked: bool | None,
        token: MistuneToken,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        markup: bool = True,
    ) -> None:
        super().__init__(
            token=token,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            markup=markup,
        )

        self.bullet = bullet
        self.checked = checked

    # compose
    @override
    def compose(self) -> ComposeResult:
        # Checkbox
        if self.checked == None:
            yield Static(self.bullet)
        else:
            yield Static(
                "██", classes="item-checked" if self.checked else "item-unchecked"
            )

        # Content
        yield MarkdownContainerBlock(self.token)


# Markdown list
class MarkdownList(MarkdownContainerBlock):
    """Markdown list"""

    # compose
    @override
    def compose(self) -> ComposeResult:
        start = self.token.attrs.get("start") or 1  # int

        # For every item
        for index, item in enumerate(self.token.children, start=start):  # pyright: ignore[reportArgumentType]
            if self.token.attrs.get("ordered"):
                bullet = f"{index}."
            else:
                if self.token.attrs.get("depth") == 0:
                    bullet = "•"
                else:
                    bullet = "◦"

            # Render
            yield MarkdownListItem(bullet, item.attrs.get("checked"), item)  # pyright: ignore[reportArgumentType]


# Markdown block text
class MarkdownBlockText(MarkdownLeafBlock):
    """Markdown block text"""


# Markdown table
class MarkdownTable(MarkdownLeafBlock):
    """Markdown table"""

    # render
    @override
    def render(self) -> RenderResult:
        table = Table(expand=False)

        # For every item
        for child in self.token.children:
            match child.type:
                case "table_head":
                    for cell in child.children:
                        table.add_column(self.render_cell(cell))

                case "table_body":
                    for row in child.children:
                        table.add_row(
                            *[self.render_cell(cell) for cell in row.children]
                        )

                case _:
                    continue

        # Return
        return table

    # render_cell
    def render_cell(self, cell: MistuneToken) -> RenderableType:
        # HACK: Manually align content inside a table
        # because the contents are not guaranteed to be a text always.
        return Align(
            renderable=self.render_inlines(cell.children),
            align=cell.attrs.get("align") or "left",  # pyright: ignore[reportArgumentType]
        )


# Markdown math
class MarkdownMath(MarkdownLeafBlock):
    # CSS
    DEFAULT_CSS: ClassVar[str] = """
    MarkdownMath {
      content-align: center middle;
    }
    """

    # render
    @override
    def render(self) -> RenderResult:
        return pretty(parse_latex(self.token.raw))  # pyright: ignore[reportUnknownVariableType]


# Markdown slide
class MarkdownSlide(Widget):
    """Markdown slide"""

    slide: MistuneToken

    # __init__
    def __init__(
        self,
        slide: MistuneToken,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        markup: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            markup=markup,
        )

        self.slide = slide

    # compose
    @override
    def compose(self) -> ComposeResult:
        yield MarkdownRoot(self.slide)
