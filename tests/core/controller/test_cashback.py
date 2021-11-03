from uuid import uuid4

import pytest
from sqlmodel import Session

from backend.core import controller
from backend.core.helpers.exceptions import NotFoundError
from tests.factories.sale import CreateSaleFactory
from tests.factories.seller import CreateSellerFactory


def test_get_sale_cashback_success(session: Session):
    # Prepare
    seller = controller.seller.create(session, CreateSellerFactory())
    sale = controller.sale.create(session, CreateSaleFactory(), seller)

    # Get
    sale_cashback = controller.cashback.get_sale_cashback(session, sale)

    # Assert
    assert sale_cashback.sale_id == sale.id
    assert sale_cashback.cashback_value < sale.value
    assert sale_cashback.cashback_percentual <= 1


def test_get_sale_cashback_by_id_success(session: Session):
    # Prepare
    seller = controller.seller.create(session, CreateSellerFactory())
    sale = controller.sale.create(session, CreateSaleFactory(), seller)

    # Get
    sale_cashback = controller.cashback.get_sale_cashback_by_id(session, sale.id)

    # Assert
    assert sale_cashback.sale_id == sale.id
    assert sale_cashback.cashback_value < sale.value
    assert sale_cashback.cashback_percentual <= 1


def test_get_sale_cashback_by_id_fail(session: Session):
    with pytest.raises(NotFoundError):
        controller.cashback.get_sale_cashback_by_id(session, uuid4())


def test_get_seller_cashback_by_id_sucess(session: Session):
    # Prepare
    seller = controller.seller.create(session, CreateSellerFactory())

    # Get
    seller_cashback = controller.cashback.get_seller_cashback_by_id(session, seller.id)

    # Assert
    assert seller_cashback.seller_id == seller.id
    assert seller_cashback.seller_cpf == seller.cpf


def test_get_seller_cashback_by_id_fail(session: Session):
    with pytest.raises(NotFoundError):
        controller.cashback.get_seller_cashback_by_id(session, uuid4())
