from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session, create_engine

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
