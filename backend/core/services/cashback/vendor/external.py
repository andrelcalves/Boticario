from typing import Dict

import requests
from pydantic import AnyHttpUrl

from backend.core.config import settings
from backend.core.helpers.exceptions import ServiceError

from .. import CashbackClient


class ExternalCashbackClient(CashbackClient):
    base_url: AnyHttpUrl = settings.CASHBACK_API_URL
    api_token: str = settings.CASHBACK_API_TOKEN

    @classmethod
    def get_total(cls, seller_cpf: str) -> float:
        response = requests.get(
            f"{cls.base_url}/v1/cashback",
            params={"cpf": seller_cpf},
            headers=cls._get_headers(),
        )

        data = response.json()

        if data["statusCode"] != 200:
            raise ServiceError("external-cashback-client", data.get("message", "Unknow error in Cashback API"))

        return data["body"]["credit"]

    def _get_headers(cls) -> Dict[str, str]:
        return {"token": cls.api_token}
