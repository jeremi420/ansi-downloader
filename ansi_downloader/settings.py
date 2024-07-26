import os
from typing import Annotated
from pydantic import AfterValidator
from pydantic_settings import BaseSettings


def create_dir_if_not_exist(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


class Settings(BaseSettings):
    subtitles_directory: Annotated[str, AfterValidator(create_dir_if_not_exist)] = (
        "./subtitles"
    )
