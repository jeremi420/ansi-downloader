from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    subtitles_directory: str = "./subtitles"
