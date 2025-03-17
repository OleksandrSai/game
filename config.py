from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from enums import LoadSource


class Settings(BaseSettings):
    LOAD_SOURCE: LoadSource = LoadSource.LOCAL
    SOURCE_LOAD_PATH: str = "settings/files/"
    LINK_API: str = "/api/"


load_dotenv()
settings = Settings()
