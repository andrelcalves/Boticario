from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.core import controller
from backend.core.security.authorization import load_authorization
from tests.factories.seller import CreateSellerFactory


def test_get_access_token_success(client: TestClient, session: Session):
    # Prepare
    schema = CreateSellerFactory()
    controller.seller.create(session, schema)

    # Request
    response = client.post("/auth/token", data={"username": schema.cpf, "password": schema.password})
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert load_authorization(data.get("access_token", ""))


def test_get_access_token_fail(client: TestClient, session: Session):
    # Prepare
    schema = CreateSellerFactory()
    controller.seller.create(session, schema)

    # Request
    response = client.post("/auth/token", data={"username": schema.cpf, "password": "wrongpassword"})
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert data.get("access_token") is None


def test_get_access_token_with_invalid_cpf_fail(client: TestClient, session: Session):
    # Prepare
    schema = CreateSellerFactory()
    schema2 = CreateSellerFactory()
    controller.seller.create(session, schema)

    # Request

    response = client.post("/auth/token", data={"username": schema2.cpf, "password": schema.password})
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert data.get("access_token") is None
