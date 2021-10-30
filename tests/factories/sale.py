import datetime as dt

import factory

from backend.core.models import CreateSale


class CreateSaleFactory(factory.Factory):
    saller_cpf: str
    value: float = factory.Faker("pyfloat", positive=True)
    item_code: str = factory.Faker("pystr")
    date: dt.date = factory.Faker("date")

    class Meta:
        model = CreateSale
