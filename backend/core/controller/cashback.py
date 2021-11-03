from uuid import UUID

from sqlmodel import Session, extract, select

from backend.core.helpers.constants import SalesCashbackRange
from backend.core.models import Sale, Seller, SellerCashback
from backend.core.models.cashback import SaleCashback
from backend.core.services import DefaultCashbackClient

from . import sale as sale_controller
from . import seller as seller_controller


def get_sale_cashback(session: Session, sale: Sale) -> SaleCashback:
    sales = session.exec(
        select(Sale)
        .join(Seller)
        .where(
            Seller.id == sale.seller.id,
            extract("month", Sale.date) == sale.date.month,
            extract("year", Sale.date) == sale.date.year,
        )
    ).all()

    total_sales = sum(s.value for s in sales)

    percentual = SalesCashbackRange.get_percentual_by_total_value(total_sales)
    value = sale.value * percentual

    return SaleCashback(cashback_value=value, cashback_percentual=percentual, sale_id=sale.id)


def get_sale_cashback_by_id(session: Session, sale_id: UUID) -> SaleCashback:
    sale = sale_controller.get_by_id(session, sale_id)

    return get_sale_cashback(session, sale)


def get_seller_cashback_by_id(session: Session, seller_id: UUID) -> SellerCashback:
    seller = seller_controller.get_by_id(session, seller_id)
    total_cashback = DefaultCashbackClient.get_total(seller.cpf)

    data = {
        "seller_id": seller.id,
        "seller_name": seller.name,
        "seller_cpf": seller.cpf,
        "total_cashback": total_cashback,
    }

    return SellerCashback(**data)
