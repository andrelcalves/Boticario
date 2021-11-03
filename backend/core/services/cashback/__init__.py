from abc import ABC, abstractclassmethod


class CashbackClient(ABC):
    @abstractclassmethod
    def get_total(cls, seller_cpf: str) -> float:
        raise NotImplementedError
