from dataclasses import dataclass
from typing import Literal
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import quote

import requests


@dataclass
class Subtitles:
    original_title: str
    english_title: str
    alternative_title: str


SearchType = Literal["original_title", "english_title", "alternative_title"]


def search_ansi(
    search_term: str, search_type: SearchType = "original_title", page: int = 1
):
    url = f"http://animesub.info/szukaj.php?szukane={quote(search_term)}&pTitle={search_type_to_param(search_type)}&od={page - 1}"
    response = requests.get(url)
    return response.content.decode("cp1250")


def search_type_to_param(search_type: SearchType):
    if search_type == "english_title":
        return "en"
    if search_type == "original_title":
        return "org"
    return "pl"


def parse_subtitles_list(html: str):
    soup = BeautifulSoup(html, "html.parser")
    subtitles_tags = soup.find_all("table", class_="Napisy")[1:]
    subtitles: list[Subtitles] = []
    for tag in subtitles_tags:
        original_title = tag.css.select("tr:nth-child(1) > td:nth-child(1)")[0].string
        english_title = tag.css.select("tr:nth-child(2) > td:nth-child(1)")[0].string
        alternative_title = tag.css.select("tr:nth-child(3) > td:nth-child(1)")[
            0
        ].string
        alternative_title = tag.css.select("tr:nth-child(3) > td:nth-child(1)")[
            0
        ].string
        subtitles.append(
            Subtitles(
                original_title=original_title,
                english_title=english_title,
                alternative_title=alternative_title,
            )
        )
    return subtitles


def main():
    response = search_ansi("space dandy")
    print(parse_subtitles_list(response))


if __name__ == "__main__":
    main()
