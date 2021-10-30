import json

from fastapi import status
from fastapi.testclient import TestClient

from backend.core.helpers.constants import SaleStatusEnum
from backend.core.models import Sale
from tests.factories.sale import CreateSaleFactory

# Em uma aplicação real, todos os testes seriam implementados
# implementei apenas o 1 caso para demonstrar como realizo os testes de ingração


def test_create_sale_success(client: TestClient, access_token: str):
    # Prepare
    schema = CreateSaleFactory()

    # Request
    response = client.post(
        "/v1/sales/",
        json=json.loads(schema.json()),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    data = response.json()
    sale = Sale(**data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert sale.value == schema.value
    assert sale.date == schema.date


def test_create_sale_fail(client: TestClient, access_token: str):
    # Prepare
    schema = CreateSaleFactory()

    # Request
    response = client.post("/v1/sales/", json=json.loads(schema.json()))

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_sale_success(client: TestClient, access_token: str):
    # Prepare
    schema = CreateSaleFactory()

    # Request
    response = client.post(
        "/v1/sales/", json=json.loads(schema.json()), headers={"Authorization": f"Bearer {access_token}"}
    )
    created_sale = response.json()

    response = client.patch(
        "/v1/sales/",
        json={"id": created_sale["id"], "status": SaleStatusEnum.APROVED.value},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json()
    sale = Sale(**data)

    # Assert
    assert sale.status == SaleStatusEnum.APROVED


def test_delete_sale_success(client: TestClient, access_token: str):
    # Prepare
    schema = CreateSaleFactory()

    # Request
    created_response = client.post(
        "/v1/sales/", json=json.loads(schema.json()), headers={"Authorization": f"Bearer {access_token}"}
    )

    created_sale = created_response.json()

    delete_response = client.delete(
        f"/v1/sales/{created_sale['id']}", headers={"Authorization": f"Bearer {access_token}"}
    )
    deleted_sale = delete_response.json()

    get_sale_response = client.get(
        f"/v1/sale/{created_sale['id']}", headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert
    assert deleted_sale["id"] == created_sale["id"]
    assert get_sale_response.status_code == status.HTTP_404_NOT_FOUND
