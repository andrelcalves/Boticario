from typing import List
from uuid import UUID

from sqlmodel import Session, extract, select

from backend.core.config import settings
from backend.core.helpers.constants import SaleStatusEnum
from backend.core.helpers.exceptions import DatabaseError, NotFoundError
from backend.core.models import CreateSale, GetAllSales, Sale, Seller


def get_by_id(session: Session, sale_id: UUID) -> Sale:
    sale = session.exec(select(Sale).where(Sale.id == sale_id)).first()

    if not sale:
        raise NotFoundError(f"Couldn't find sale with id {sale_id}")

    return sale


def get_all(session: Session, schema: GetAllSales) -> List[Sale]:
    args = []

    if schema.month and schema.year:
        args.extend([extract("month", Sale.date) == schema.month, extract("year", Sale.date) == schema.year])

    if schema.seller_cpf:
        args.append(Sale.seller_cpf == schema.seller_cpf)

    return session.exec(select(Sale).where(*args)).all()


def create(session: Session, schema: CreateSale, seller: Seller) -> Sale:
    sale = Sale(**schema.dict(), seller_cpf=seller.cpf)

    if sale.seller_cpf in settings.CPFS_TO_AUTO_APROVE_SALES:
        sale.status = SaleStatusEnum.APROVED

    session.add(sale)
    session.commit()
    return sale


def delete_by_id(session: Session, sale_id: UUID) -> Sale:
    sale = get_by_id(session, sale_id)

    if sale.status != SaleStatusEnum.PENDING:
        raise DatabaseError(f"You can only delete sales with pending status! Current status: {sale.status}")

    session.delete(sale)

    return sale


def update_sale_status_by_id(session: Session, sale_id: UUID, status: SaleStatusEnum) -> Sale:
    sale = get_by_id(session, sale_id)

    if sale.status != SaleStatusEnum.PENDING:
        raise DatabaseError(f"You can only update sales with pending status! Current status: {sale.status}")

    sale.status = status
    session.add(sale)
    session.commit()

    return sale


def get_total_of_sales_by_period(session, seller_id: UUID, month: int, year: int) -> float:
    sales = session.exec(
        select(Sale)
        .join(Seller)
        .where(
            Seller.id == seller_id,
            extract("month", Sale.date) == month,
            extract("year", Sale.date) == year,
        )
    ).all()
    return sum(s.value for s in sales)
