from typing import Dict

import requests
from pydantic import AnyHttpUrl

from backend.core.config import settings

from .. import CashbackClient


class ExternalCashbackClient(CashbackClient):
    base_url: AnyHttpUrl = settings.CASHBACK_API_URL
    api_token: str = settings.CASHBACK_API_TOKEN

    def get_total(self, seller_cpf: str) -> float:
        response = requests.get(
            f"{self.base_url}/v1/cashback",
            params={"cpf": seller_cpf},
            headers=self.__headers,
        )
        response.raise_for_status()
        data = response.json()

        return data["body"]["credit"]

    @property
    def __headers(self) -> Dict[str, str]:
        return {"token": self.api_token}
