from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from backend.core.helpers.exceptions import NotFoundError
from backend.core.models.seller import CreateSeller

from .. import controller
from ..config import settings

engine = create_engine(
    settings.SQLALCHEMY_DB_URI, connect_args={"connect_timeout": settings.SQLALCHEMY_CONNECTION_TIMEOUT}
)


def make_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()

        except Exception as err:
            session.rollback()
            raise err


@contextmanager
def session_context() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()

        except Exception as err:
            session.rollback()
            raise err


def init_database() -> None:
    SQLModel.metadata.create_all(engine)

    with session_context() as session:
        try:
            controller.seller.get_by_cpf(session, settings.FIRST_SELLER_CPF)

        except NotFoundError:
            controller.seller.create(
                session,
                CreateSeller(
                    cpf=settings.FIRST_SELLER_CPF,
                    name=settings.FIRST_SELLER_NAME,
                    email=settings.FIRST_SELLER_EMAIL,
                    password=settings.FIRST_SELLER_PASSWORD,
                    confirm_password=settings.FIRST_SELLER_PASSWORD,
                ),
            )
