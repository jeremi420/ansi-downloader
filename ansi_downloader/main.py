from dataclasses import dataclass
from typing import Literal
from requests import get
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag
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
    subtitles_elements: list[Tag] = soup.find_all("table", class_="Napisy")[1:]
    subtitles: list[Subtitles] = []
    for element in subtitles_elements:
        subtitles.append(parse_subtitles_item(element))
    return subtitles


def parse_subtitles_item(container: Tag):
    original_title = container.findAll("tr")[0].find("td").string
    english_title = container.findAll("tr")[1].find("td").string
    alternative_title = container.findAll("tr")[2].find("td").string

    return Subtitles(
        original_title=original_title,
        english_title=english_title,
        alternative_title=alternative_title,
    )


def main():
    response = search_ansi("space dandy")
    subtitles = parse_subtitles_list(response)
    print(subtitles[0])


if __name__ == "__main__":
    main()
