from enum import Enum


class EnvironmentEnum(str, Enum):
    production: str = "prod"
    homologation: str = "hml"
    development: str = "dev"
    testing: str = "test"


class SaleStatusEnum(str, Enum):
    REFUSED: str = "Recusado"
    APROVED: str = "Aprovado"
    PENDING: str = "Em validação"


class SalesCashbackRange:
    PERCENTUAL_BY_VALUE = {1500: 0.2, 1000: 0.15, 0: 0.1}

    @classmethod
    def get_percentual_by_total_value(cls, total: float) -> float:
        sorted_values = sorted(cls.PERCENTUAL_BY_VALUE.items(), key=lambda x: x[0], reverse=True)
        return next((p for v, p in sorted_values if total > v))
