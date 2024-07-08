from dataclasses import dataclass
from requests import get
from bs4 import BeautifulSoup


@dataclass
class Subtitles:
    original_title: str
    english_title: str
    alternative_title: str


def main():
    start_url = "http://animesub.info/szukaj_old.php?szukane=+&pTitle=org"
    response = get(start_url)
    soup = BeautifulSoup(response.content.decode("cp1250"), "html.parser")
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
    print(subtitles)


if __name__ == "__main__":
    main()
