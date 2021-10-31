from uuid import UUID

from sqlmodel import Session, exists, select

from backend.core.helpers.documents import normalize_cpf
from backend.core.helpers.exceptions import DatabaseError, NotFoundError
from backend.core.models import CreateSeller, Seller
from backend.core.security.hash import get_password_hash


def get_by_cpf(session: Session, seller_cpf: str) -> "Seller":
    cpf = normalize_cpf(seller_cpf)
    seller = session.exec(select(Seller).where(Seller.cpf == cpf)).first()

    if not seller:
        raise NotFoundError(f"Could'nt found seller with cpf {cpf}")

    return seller


def get_by_id(session: Session, seller_id: UUID) -> "Seller":
    seller = session.exec(select(Seller).where(Seller.id == seller_id)).first()

    if not seller:
        raise NotFoundError(f"Could'nt found seller with ID {seller_id}")

    return seller


def create(session: Session, schema: "CreateSeller") -> "Seller":
    if session.exec(select(Seller).where(Seller.cpf == schema.cpf)).first():
        raise DatabaseError(f'Alread exists Seller with CPF "{schema.cpf}"')

    data = schema.dict(exclude={"confirm_password": ...})
    data["password_hash"] = get_password_hash(data.pop("password"))

    seller = Seller(**data)
    session.add(seller)
    session.commit()

    return seller


def check_if_exists(session: Session, seller_id: UUID) -> bool:
    return session.exec(select(exists().where(Seller.id == seller_id))).first()
