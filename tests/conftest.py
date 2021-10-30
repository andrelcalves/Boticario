from typing import Generator

import pytest
from _pytest.config import Config
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from backend.app import app
from backend.core import controller
from backend.core.config import ENVIRONMENT, settings
from backend.core.helpers.constants import EnvironmentEnum
from backend.core.helpers.database import engine, make_session
from backend.core.helpers.documents import normalize_cpf
from backend.core.helpers.exceptions import NotFoundError
from backend.core.models import Seller
from backend.core.security.authorization import create_access_token
from tests.factories.seller import CreateSellerFactory


def pytest_configure(config: Config):
    if ENVIRONMENT != EnvironmentEnum.testing:
        raise RuntimeError(f"You should run tests only in test environment! Current environment: {ENVIRONMENT.name}")

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


@pytest.fixture(scope="session")
def session() -> Generator[Session, None, None]:
    yield next(make_session())


@pytest.fixture(scope="session")
def seller_to_auto_aprove_sales(session: Session) -> Seller:
    cpf = normalize_cpf("153.509.460-56")

    if cpf not in settings.CPFS_TO_AUTO_APROVE_SALES:
        settings.CPFS_TO_AUTO_APROVE_SALES.append(cpf)

    try:
        seller = controller.seller.get_by_cpf(session, cpf)

    except NotFoundError:
        seller = controller.seller.create(session, CreateSellerFactory(cpf=cpf))

    yield seller


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def access_token(session: Session) -> str:
    seller = controller.seller.get_by_cpf(session, settings.FIRST_SELLER_CPF)
    token = create_access_token(str(seller.id))

    yield token.access_token
