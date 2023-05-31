"""Utilities for working with generic URLs."""

from __future__ import annotations

import pathlib
import time
import typing

import requests
import rich.progress
import typer
from rich import print

import wayback_utils

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

# These paths assume we run in the main repo directory.
URLS_SUBMITTED_FILE = pathlib.Path().resolve() / "urls_submitted.txt"
URLS_TO_SUBMIT_FILE = pathlib.Path().resolve() / "urls_to_submit.txt"


def read_urls_from_file(file_path: pathlib.Path) -> set[str]:
    if not file_path.exists():
        return set()

    with file_path.open("r") as file:
        return {line.strip() for line in file}


def write_urls_to_file(
    urls: set[str],
    file_path: pathlib.Path,
) -> None:
    import typer

    print(f"{len(urls)} urls to submit.")

    with file_path.open("w") as file:
        file.writelines(f"{url}\n" for url in urls)


def read_urls_to_submit_from_file() -> set[str]:
    return read_urls_from_file(file_path=URLS_TO_SUBMIT_FILE)


def write_urls_to_submit_to_file(urls: set[str]) -> None:
    write_urls_to_file(
        urls=urls,
        file_path=URLS_TO_SUBMIT_FILE,
    )


def read_submitted_urls_from_file() -> set[str]:
    return read_urls_from_file(file_path=URLS_SUBMITTED_FILE)


def write_submitted_urls_to_file(urls: set[str]) -> None:
    write_urls_to_file(
        urls=urls,
        file_path=URLS_SUBMITTED_FILE,
    )


def check_url_archived(url: str) -> bool:
    api_url = f"http://archive.org/wayback/available?url={url}"
    response = requests.get(api_url)
    data = response.json()
    return bool("archived_snapshots" in data and data["archived_snapshots"])


def submit_url(url: str) -> bool:
    payload = {"url": url}
    response = requests.post("https://web.archive.org/save", data=payload)
    return response.status_code == 200


@app.command()
def submit() -> None:
    """Submit landed urls to Wayback Machine if not already submitted."""
    urls_to_submit = read_urls_to_submit_from_file()
    submitted_urls = read_submitted_urls_from_file()

    urls_to_submit = {url for url in urls_to_submit if url not in submitted_urls}

    urls_failed_to_submit = set()

    for url in rich.progress.track(
        sequence=urls_to_submit,
        description="Submitting new urls...",
    ):
        try:
            if not check_url_archived(url) and submit_url(url):
                urls_failed_to_submit.add(url)
            else:
                submitted_urls.add(url)
            # Limit rate to 5 of these 2 requests per minute, 10 requests per minute.
            # Should be less than their limit of 15 requests per minute.
            time.sleep(6)
        except Exception as e:
            wayback_utils.ERR_CONSOLE.print(f"Error processing url {url}!")
            wayback_utils.ERR_CONSOLE.print(e)
            wayback_utils.ERR_CONSOLE.print("Continuing...")

    # Update file with submitted urls.
    write_submitted_urls_to_file(submitted_urls)

    # Overwrite file with urls to submit.
    write_urls_to_submit_to_file(set())


@app.callback()
def main(
    *,
    version: bool | None = typer.Option(
        False,
        "--version",
        "-v",
        help=f"print the version of {wayback_utils.__name__}",
        callback=wayback_utils.version_callback,
        is_eager=True,
    ),
) -> None:
    """Utilities for working with generic URLs."""
    pass


if __name__ == "__main__":
    app()
