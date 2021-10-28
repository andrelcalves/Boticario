from enum import Enum


class EnvironmentEnum(str, Enum):
    production: str = "prod"
    homologation: str = "hml"
    development: str = "dev"
    testing: str = "test"
