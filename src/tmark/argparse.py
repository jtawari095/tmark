# pyright: reportUninitializedInstanceVariable=false
# pyright: reportUnknownMemberType=false

from pathlib import Path
from typing import override

from tap import Positional, Tap


# Argument parser
class ArgumentParser(Tap):
    source: Positional[Path]  # path to the markdown source file
    theme: str = "gruvbox"  # theme to use

    # configure
    @override
    def configure(self) -> None:
        self.add_argument("-t", "--theme")
