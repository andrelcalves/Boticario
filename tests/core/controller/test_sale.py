from datetime import date
from uuid import uuid4

import pytest
from sqlmodel import Session

from backend.core import controller
from backend.core.helpers.constants import SalesCashbackRange, SaleStatusEnum
from backend.core.helpers.exceptions import DatabaseError, NotFoundError
from backend.core.models import GetAllSales, Seller
from tests.factories.sale import CreateSaleFactory
from tests.factories.seller import CreateSellerFactory


def test_create_sale_success(session: Session):
    # Prepare
    seller = controller.seller.create(session, schema=CreateSellerFactory())
    schema = CreateSaleFactory()

    # Create
    sale = controller.sale.create(session, schema, seller)

    # Assert
    assert sale.seller_cpf == seller.cpf
    assert sale.value == schema.value
    assert sale.date is not schema.date
    assert sale.item_code == schema.item_code
    assert sale.status == SaleStatusEnum.PENDING
    assert sale.cashback_value is not None
    assert sale.cashback_percentual is not None


def test_create_sale_auto_aprove_success(session: Session, seller_to_auto_aprove_sales: Seller):
    # Prepare
    schema = CreateSaleFactory()

    # Create
    sale = controller.sale.create(session, schema, seller_to_auto_aprove_sales)

    # Assert
    assert sale.status == SaleStatusEnum.APROVED


def test_get_all_success(session: Session):
    # Prepare
    today = date.today()
    seller = controller.seller.create(session, schema=CreateSellerFactory())

    sales_schema = [
        CreateSaleFactory(seller_cpf=seller.cpf, date=date(day=i, month=today.month, year=today.year))
        for i in range(1, 11)
    ]

    # Create
    for schema in sales_schema:
        controller.sale.create(session, schema, seller)

    sales = controller.sale.get_all(session, GetAllSales(seller_cpf=seller.cpf, month=today.month, year=today.year))

    # assert
    assert len(sales) >= 10
    assert all(s.date.month == today.month and s.date.year == today.year for s in sales)

    for sale in sales_schema:
        assert any(s.date == sale.date for s in sales)
        assert any(s.value == sale.value for s in sales)
        assert any(s.item_code == sale.item_code for s in sales)


def test_delete_success(session: Session):
    # Prepare
    seller = controller.seller.create(session, schema=CreateSellerFactory())
    sale = controller.sale.create(session, CreateSaleFactory(), seller)

    # Delete
    deleted_sale = controller.sale.delete_by_id(session, sale.id)

    # Assert
    assert deleted_sale is not None
    assert deleted_sale.id == sale.id
    assert deleted_sale == sale

    with pytest.raises(NotFoundError):
        controller.sale.get_by_id(session, sale.id)


def test_delete_fail(session: Session):
    with pytest.raises(NotFoundError):
        controller.sale.get_by_id(session, uuid4())


def test_sale_cashback(session: Session):
    # Prepare
    seller = controller.seller.create(session, schema=CreateSellerFactory())

    # Create
    sale_range1 = controller.sale.create(session, CreateSaleFactory(value=1), seller)
    sale_range2 = controller.sale.create(session, CreateSaleFactory(value=1000), seller)
    sale_range3 = controller.sale.create(session, CreateSaleFactory(value=1500), seller)

    # Assert

    assert sale_range1.cashback_percentual == SalesCashbackRange.get_percentual_by_total_value(1)
    assert sale_range2.cashback_percentual == SalesCashbackRange.get_percentual_by_total_value(1000)
    assert sale_range3.cashback_percentual == SalesCashbackRange.get_percentual_by_total_value(1500)


def test_update_sale_status_success(session: Session):
    # Prepare
    seller = controller.seller.create(session, schema=CreateSellerFactory())
    sale = controller.sale.create(session, CreateSaleFactory(status=SaleStatusEnum.PENDING), seller)
    sale2 = controller.sale.create(session, CreateSaleFactory(status=SaleStatusEnum.PENDING), seller)

    # Update
    controller.sale.update_sale_status_by_id(session, sale.id, status=SaleStatusEnum.APROVED)
    controller.sale.update_sale_status_by_id(session, sale2.id, status=SaleStatusEnum.REFUSED)

    # Assert
    assert sale.status == SaleStatusEnum.APROVED
    assert sale2.status == SaleStatusEnum.REFUSED


def test_update_sale_status_fail(session: Session):
    # Prepare
    seller = controller.seller.create(session, schema=CreateSellerFactory())
    sale = controller.sale.create(session, CreateSaleFactory(status=SaleStatusEnum.PENDING), seller)

    # Update
    controller.sale.update_sale_status_by_id(session, sale.id, status=SaleStatusEnum.APROVED)

    # Assert
    with pytest.raises(DatabaseError):
        controller.sale.update_sale_status_by_id(session, sale.id, status=SaleStatusEnum.PENDING)

    with pytest.raises(DatabaseError):
        controller.sale.update_sale_status_by_id(session, sale.id, status=SaleStatusEnum.REFUSED)
