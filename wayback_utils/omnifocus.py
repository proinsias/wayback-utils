"""Utilities for working with URLs saved to OmniFocus."""

import typing

import typer
from rich import print

import wayback_utils

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.callback()
def main(
    *,
    version: typing.Optional[bool] = typer.Option(
        False,
        "--version",
        "-v",
        help=f"print the version of {wayback_utils.__name__}",
        callback=wayback_utils.version_callback,
        is_eager=True,
    ),
) -> None:
    """Utilities for working with URLs saved to OmniFocus."""
    pass


if __name__ == "__main__":
    app()
