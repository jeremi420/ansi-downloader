from dataclasses import dataclass
from requests import get
from bs4 import BeautifulSoup


@dataclass
class Subtitles:
    original_title: str
    english_title: str
    alternative_title: str


def parse_subtitles(html: str):
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
    start_url = "http://animesub.info/szukaj_old.php?szukane=+&pTitle=org"
    response = get(start_url)
    print(parse_subtitles(response.content.decode("cp1250")))


if __name__ == "__main__":
    main()
