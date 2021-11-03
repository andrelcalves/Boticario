from .. import CashbackClient


class NoneCashbackClient(CashbackClient):
    """
    Cliente que não executa nada, apenas implementa os metódos sem nenhuma ação
    conforme o design pattern: https://sourcemaking.com/design_patterns/null_object
    """

    @classmethod
    def get_total(cls, seller_cpf: str) -> float:
        return 1
