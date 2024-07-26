from dataclasses import dataclass
from typing import Literal
from requests import Session
from bs4 import BeautifulSoup, Tag
from urllib.parse import quote


@dataclass
class SubtitlesFile:
    file_name: str


@dataclass
class FormData:
    id: int
    sh: str


@dataclass
class Subtitles:
    original_title: str
    english_title: str
    alternative_title: str
    form_data: FormData


SearchType = Literal["original_title", "english_title", "alternative_title"]


def search_ansi(
    search_term: str,
    search_type: SearchType = "original_title",
    page: int = 1,
    session: Session = Session(),
):
    url = f"http://animesub.info/szukaj.php?szukane={quote(search_term)}&pTitle={search_type_to_param(search_type)}&od={page - 1}"
    response = session.get(url)
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
    id = container.findAll("form")[0].find("input", {"name": "id"})["value"]
    sh = container.findAll("form")[0].find("input", {"name": "sh"})["value"]

    return Subtitles(
        original_title=original_title,
        english_title=english_title,
        alternative_title=alternative_title,
        form_data=FormData(id=id, sh=sh),
    )


def download_subtitles_file(subtitles: Subtitles, session: Session = Session()):
    response = session.post(
        "http://animesub.info/sciagnij.php",
        data={"id": subtitles.form_data.id, "sh": subtitles.form_data.sh},
    )
    file_name = response.headers["content-disposition"].split("filename=")[1]
    with open(file_name, "wb") as file:
        file.write(response.content)
    return SubtitlesFile(file_name=file_name)


def main():
    session = Session()
    response = search_ansi("space dandy", session=session)
    subtitles = parse_subtitles_list(response)
    download_subtitles_file(subtitles[0], session)
    print(subtitles[0])


if __name__ == "__main__":
    main()
