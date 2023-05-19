"""Utilities for submitting URLs to the Internet Archive's Wayback Machine."""

import datetime as dt
import os
import tempfile
import typing

import rich.pretty
import typer

import wayback_utils


app = typer.Typer()
rich.pretty.install()


def version_callback(
    value: bool,
) -> None:
    if value:
        typer.echo(f"{wayback_utils.__name__} version: {wayback_utils.__version__}")
        raise typer.Exit()


@app.command()
def main(
    *,
    version: typing.Optional[bool] = typer.Option(
        False,
        "--version",
        "-v",
        help=f"print the version of {wayback_utils.__name__}",
        callback=version_callback,
        is_eager=True,
    ),
    field: typing.Optional[str] = typer.Option(
        'last_modified_at',
        "--field",
        "-f",
        help="the YAML field name for the date the file was last modified",
    ),
    datetime_format: typing.Optional[str] = typer.Option(
        '%Y-%m-%d %H:%M:%S',
        "--datetime-format",
        "-d",
        help="the format for the last modified date field",
    ),
) -> None:
    """Utilities for submitting URLs to the Internet Archive's Wayback Machine."""


if __name__ == "__main__":
    app()
