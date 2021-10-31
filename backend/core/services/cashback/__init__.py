from abc import ABC, abstractmethod


class CashbackClient(ABC):
    @abstractmethod
    def get_total(self, seller_cpf: str) -> float:
        raise NotImplementedError
