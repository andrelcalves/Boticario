from datetime import date

import pytest
from pydantic import ValidationError

from backend.core.models import GetAllSales
from tests.factories.sale import CreateSaleFactory


def test_get_all_schema_fail():
    today = date.today()

    with pytest.raises(ValidationError):
        GetAllSales(month=0, year=today.year)

    with pytest.raises(ValidationError):
        GetAllSales(month=13, year=today.year)

    with pytest.raises(ValidationError):
        GetAllSales(month=None, year=today.year)

    with pytest.raises(ValidationError):
        GetAllSales(month=today.month, year=None)


def test_create_sale_with_invalid_value_fail():
    with pytest.raises(ValidationError):
        CreateSaleFactory(value=None)

    with pytest.raises(ValidationError):
        CreateSaleFactory(value=-1)


def test_create_sale_with_invalid_item_code_fail():
    with pytest.raises(ValidationError):
        CreateSaleFactory(item_code=None)

    with pytest.raises(ValidationError):
        CreateSaleFactory(item_code="")
