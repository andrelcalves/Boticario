from pydantic import BaseSettings
from pydantic.networks import PostgresDsn

from .helpers.constants import EnvironmentEnum


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmentEnum
    VERSION: str = "0.0.0"

    SQLALCHEMY_DB_URI: PostgresDsn

    class Config:
        env_file: str = ".env"


settings = Settings()

ENVIRONMENT = settings.ENVIRONMENT
