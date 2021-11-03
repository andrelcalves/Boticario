import pytest
from pydantic import ValidationError

from tests.factories.seller import CreateSellerFactory


def test_create_seller_model_with_invalid_cpf_fail():
    with pytest.raises(ValidationError):
        CreateSellerFactory(cpf="1234")


def test_create_seller_model_with_invalid_confirm_password_fail():
    with pytest.raises(ValidationError):
        CreateSellerFactory(cpf="1234", confirm_password="1")
