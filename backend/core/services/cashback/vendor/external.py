from typing import Dict

import requests
from pydantic import AnyHttpUrl

from backend.core.config import settings
from backend.core.helpers.exceptions import ServiceError

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

        data = response.json()

        if data["statusCode"] != 200:
            raise ServiceError(data.get("message", "Unknow error in Cashback API"))

        return data["body"]["credit"]

    @property
    def __headers(self) -> Dict[str, str]:
        return {"token": self.api_token}
