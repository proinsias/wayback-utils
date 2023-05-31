"""Utilities for submitting URLs to the Internet Archive's Wayback Machine."""

import rich.console
from rich import print

# Keep these in sync with CHANGELOG.md and pyproject.toml.
__name__ = "wayback-utils"
__pkg_name__ = "wayback_utils"
__version__ = "0.1.0"

ERR_CONSOLE = rich.console.Console(stderr=True)


def version_callback(value: bool) -> None:
    import typer

    if value:
        print(
            f"{__name__} version: {__version__}",
        )
        raise typer.Exit()
