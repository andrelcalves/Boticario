from typing import List

from pydantic import BaseSettings, PositiveInt, validator
from pydantic.networks import EmailStr, PostgresDsn

from .helpers.constants import EnvironmentEnum
from .helpers.documents import normalize_cpf


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmentEnum
    VERSION: str = "0.0.0"

    # Database
    SQLALCHEMY_DB_URI: PostgresDsn
    SQLALCHEMY_CONNECTION_TIMEOUT: PositiveInt = 30

    # Application
    APPLICATION_NAME: str = "backend-boticario"
    HOST: str = "localhost"
    PORT: PositiveInt = 5000
    WORKERS: PositiveInt = 2
    DEBUG: bool = False
    BASE_PATH: str = ""
    LOG_LEVEL: str = "info"
    FIRST_SELLER_CPF: str
    FIRST_SELLER_NAME: str
    FIRST_SELLER_PASSWORD: str
    FIRST_SELLER_EMAIL: EmailStr

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Options
    DEFAULT_TIMEZONE: str = "America/Sao_Paulo"
    CPFS_TO_AUTO_APROVE_SALES: List[str] = '["153.509.460-56"]'

    @validator("CPFS_TO_AUTO_APROVE_SALES", pre=True)
    def normalize_cpfs_to_auto_aprove_sales(cls, value: str) -> List[str]:
        return [normalize_cpf(cpf) for cpf in value]

    class Config:
        env_file: str = ".env"


settings = Settings()

ENVIRONMENT = settings.ENVIRONMENT
