from fastapi import status
from fastapi.testclient import TestClient

from backend.core.models import Seller
from tests.factories.seller import CreateSellerFactory


def test_create_seller_success(client: TestClient, access_token: str):
    # Prepare
    schema = CreateSellerFactory()

    # Request
    response = client.post(
        "/v1/seller/", json=schema.dict(), allow_redirects=True, headers={"Authorization": f"Bearer {access_token}"}
    )
    seller = Seller(**response.json())

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert seller.cpf == schema.cpf
    assert seller.email == schema.email


def test_create_seller_fail(client: TestClient, access_token: str):
    # Prepare
    schema = CreateSellerFactory()

    # Request
    response = client.post(
        "/v1/seller/",
        json=schema.dict(),
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
