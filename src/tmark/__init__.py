from pathlib import Path
from typing import final, override

import mistune
import more_itertools
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.driver import Driver
from textual.reactive import reactive
from textual.types import CSSPathType
from textual.widgets import ContentSwitcher

from tmark.argparse import ArgumentParser
from tmark.components.slide import MarkdownSlide
from tmark.token import MistuneToken


# Tmark
@final
class Tmark(App[None]):
    slides: list[MistuneToken]
    position: reactive[int] = reactive(1, init=False)

    # Bindings
    BINDINGS = [
        Binding("right", "next", "Go to next slide"),
        Binding("left", "previous", "Go to previous slide"),
    ]

    # CSS
    CSS_PATH = "./styles/app.css"

    # __init__
    def __init__(
        self,
        source: Path,
        theme: str,
        driver_class: type[Driver] | None = None,
        css_path: CSSPathType | None = None,
        watch_css: bool = False,
        ansi_color: bool = False,
    ):
        super().__init__(
            driver_class=driver_class,
            css_path=css_path,
            watch_css=watch_css,
            ansi_color=ansi_color,
        )

        with open(source, "r") as f:
            # Read and parse AST tokens
            ast_tokens = mistune.create_markdown(
                renderer="ast",
                plugins=["strikethrough", "url", "task_lists", "table", "math"],
            )(f.read())

            # dict[str, Any] is really annoying to work with when you have analyzer
            # so we will model it into our little type
            tokens = map(lambda token: MistuneToken.model_validate(token), ast_tokens)

            # Split the tokens into different slides at thematic breaks
            slides = more_itertools.split_at(
                tokens, lambda token: token.type == "thematic_break"
            )

        # Map every raw slide tokens into slide root node
        self.slides = list(
            map(lambda tokens: MistuneToken(type="root", children=tokens), slides)
        )

        # Theme
        self.theme = theme

    # compose
    @override
    def compose(self) -> ComposeResult:
        with ContentSwitcher(initial=f"slide-{self.position}", id="content"):
            for position, slide in enumerate(self.slides, start=1):
                yield MarkdownSlide(slide, id=f"slide-{position}")

    # action_next
    def action_next(self):
        if self.position != len(self.slides):
            self.position += 1

    # action_previous
    def action_previous(self):
        if self.position != 1:
            self.position -= 1

    # watch_position
    def watch_position(self, position: int):
        self.query_one("#content", ContentSwitcher).current = f"slide-{position}"


# tmark go brrrrrr
def main() -> None:
    parser = ArgumentParser()

    # Parse args
    args = parser.parse_args()

    # Create app
    tmark = Tmark(args.source, args.theme)

    # Run app
    tmark.run()
