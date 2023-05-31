"""Utilities for working with URLs saved to Pocket."""

import os
import typing

import requests
import tqdm.contrib.concurrent
import typer
from rich import print

import medium_utils
import urls_utils
import wayback_utils

GET_URL = "https://getpocket.com/v3/get"
MAX_COUNT = 5000
SEND_URL = "https://getpocket.com/v3/send"

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


def get_credentials() -> (str, str):
    access_token = os.getenv("POCKET_ACCESS_TOKEN")
    consumer_key = os.getenv("POCKET_CONSUMER_KEY")
    # If necessary, I can update this to get the access token via script as follows:
    # https://gist.github.com/Mierdin/0996952ba02d87175f3b
    # https://gist.github.com/alexpyoung/7e241a8f3f805630f0f66a1cf0763675#file-pocket_import-L71
    # Otherwise use this service: http://reader.fxneumann.de/plugins/oneclickpocket/auth.php

    if access_token is None or consumer_key is None:
        raise ValueError("Error loading credentials from environment!")

    return access_token, consumer_key


ACCESS_TOKEN, CONSUMER_KEY = get_credentials()


def filterurl(url, char):
    """Function to prune off extra URL options."""
    try:
        return url[: url.index(char)]
    except ValueError:
        return url


def get_pocket_articles(state, offset):
    data = {
        "consumer_key": CONSUMER_KEY,
        "access_token": ACCESS_TOKEN,
        "state": state,
        "sort": "newest",  # Sort articles by newest first
        "detailType": "complete",  # Retrieve complete article details
        "count": MAX_COUNT,
        "offset": offset,
    }
    headers = {"X-Accept": "application/json"}
    response = requests.post("https://getpocket.com/v3/get", data=data, headers=headers)

    print(response)
    print(response.content)

    return response.json()["list"]


def get_all_pocket_articles(state):
    offset = 0
    count = MAX_COUNT
    articles = {}

    while count == MAX_COUNT:
        articles_list = get_pocket_articles(state, offset)
        count = len(articles_list)
        articles.update(articles_list)
        offset += count

    return articles


@app.command()
def dedup():
    """Deduplicate Pocket articles."""
    urls_to_submit = urls_utils.read_urls_to_submit_from_file()

    unique_urls = set()
    duplicate_article_ids = []

    # If an article is in the archived AND unread list,
    # we want to deduplicate the unread version.
    # So let's start with the list of archived articles.

    print("Retrieving the list of archived articles from Pocket...")

    articles = get_all_pocket_articles(state="archive")

    print(f"{len(articles)} archived articles.")

    print("Removing duplicate archived articles based on URLs...")
    for article_id, article_data in articles.items():
        full_article_url = article_data["given_url"]
        # Remove extra crap from URLS (DANGEROUS - don't remove too much!)
        article_url = filterurl(full_article_url, "?utm")

        if article_url in unique_urls:
            duplicate_article_ids.append(article_id)
        else:
            unique_urls.add(article_url)

    print("Retrieving the list of unread articles from Pocket...")

    articles = get_all_pocket_articles(state="unread")

    print(f"{len(articles)} unread articles.")

    print("Removing duplicate unread articles based on URLs...")

    medium_expanded_urls = set()

    for article_id, article_data in articles.items():
        full_article_url = article_data["given_url"]
        # Remove extra crap from URLS (DANGEROUS - don't remove too much!)
        article_url = filterurl(full_article_url, "?utm")

        if medium_utils.MEDIUM_SHORTURL_PREFIX in article_url:
            # Always add this article with a shortened url to be deleted.
            # We're going to add the expanded url later.
            duplicate_article_ids.append(article_id)

            medium_expanded_urls.add(article_data["resolved_url"])
        elif article_url in unique_urls:
            duplicate_article_ids.append(article_id)
        else:
            unique_urls.add(article_url)

    medium_expanded_urls = tqdm.contrib.concurrent.thread_map(
        medium_utils.process_medium_url,
        medium_expanded_urls,
    )

    if len(duplicate_article_ids) > 0:
        print("Deleting duplicate articles from Pocket...")
        data = {
            "consumer_key": CONSUMER_KEY,
            "access_token": ACCESS_TOKEN,
            "actions": [
                {"action": "delete", "item_id": article_id}
                for article_id in duplicate_article_ids
            ],
        }

        delete_response = requests.post(SEND_URL, json=data)

        deleted_count = delete_response.json()["action_results"].count("deleted")
        print(f"Deleted {deleted_count} duplicate articles.")

    else:
        print("No duplicate articles!")

    if len(medium_expanded_urls) > 0:
        print("Adding replacement articles for shortened Medium URLs to Pocket...")
        data = {
            "consumer_key": CONSUMER_KEY,
            "access_token": ACCESS_TOKEN,
            "actions": [{"action": "add", "url": url} for url in medium_expanded_urls],
        }

        _ = requests.post(SEND_URL, json=data)

    else:
        print("No medium urls needing expanding!")

    urls_to_submit.update(unique_urls)

    urls_utils.write_urls_to_submit_to_file(urls=urls_to_submit)


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
    """Utilities for working with URLs saved to Pocket."""
    pass


if __name__ == "__main__":
    app()
