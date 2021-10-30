import datetime as dt

import factory

from backend.core.models import CreateSale


class CreateSaleFactory(factory.Factory):
    value: float = factory.Faker("pyfloat", positive=True, max_value=2000, right_digits=2)
    item_code: str = factory.Faker("pystr")
    date: dt.date = factory.Faker("date")

    class Meta:
        model = CreateSale
