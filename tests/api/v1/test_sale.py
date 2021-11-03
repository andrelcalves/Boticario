import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from backend.core.helpers.constants import SaleStatusEnum
from backend.core.models import Sale, SaleWithCashback
from tests.factories.sale import CreateSaleFactory


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


def test_update_sale_fail(client: TestClient, access_token: str, invalid_access_token: str):
    # Prepare
    schema = CreateSaleFactory()

    # Request
    response = client.post(
        "/v1/sales/", json=json.loads(schema.json()), headers={"Authorization": f"Bearer {access_token}"}
    )
    created_sale = response.json()

    response_without_token = client.patch(
        "/v1/sales/", json={"id": created_sale["id"], "status": SaleStatusEnum.APROVED.value}
    )

    response_with_invalid_token = client.patch(
        "/v1/sales/",
        json={"id": created_sale["id"], "status": SaleStatusEnum.APROVED.value},
        headers={"Authorization": f"Bearer {invalid_access_token}"},
    )

    # Assert
    assert response_without_token.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_with_invalid_token.status_code == status.HTTP_401_UNAUTHORIZED


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
        f"/v1/sales/{created_sale['id']}", headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert
    assert deleted_sale["id"] == created_sale["id"]
    assert get_sale_response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_sale_fail(client: TestClient, access_token: str, invalid_access_token: str):
    # Prepare
    schema = CreateSaleFactory()

    # Request
    created_response = client.post(
        "/v1/sales/", json=json.loads(schema.json()), headers={"Authorization": f"Bearer {access_token}"}
    )

    created_sale = created_response.json()

    response_without_token = client.delete(f"/v1/sales/{created_sale['id']}")

    response_with_invalid_token = client.delete(
        f"/v1/sales/{created_sale['id']}", headers={"Authorization": f"Bearer {invalid_access_token}"}
    )

    get_sale_response = client.get(
        f"/v1/sales/{created_sale['id']}", headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert
    assert get_sale_response.status_code == status.HTTP_200_OK
    assert response_without_token.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_with_invalid_token.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_all_sales_success(client: TestClient, access_token: str):
    # Prepare
    schema = CreateSaleFactory()

    client.post("/v1/sales/", json=json.loads(schema.json()), headers={"Authorization": f"Bearer {access_token}"})

    # Request
    response = client.get(
        "/v1/sales/",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Prepare
    data = response.json()

    # Assert
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(SaleWithCashback.validate(sale) for sale in data)


def test_get_sale_by_id_success(client: TestClient, access_token: str):
    # Prepare
    schema = CreateSaleFactory()

    sale_response = client.post(
        "/v1/sales/",
        json=json.loads(schema.json()),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    sale_data = sale_response.json()

    # Request
    response = client.get(
        f"/v1/sales/{sale_data['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == sale_data["id"]
    assert Sale.validate(data)


def test_get_sale_by_id_fail(client: TestClient, access_token: str, invalid_access_token: str):
    # Prepare
    sale_id = uuid4()

    # Request
    response = client.get(
        f"/v1/sales/{sale_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response_without_token = client.get(
        f"/v1/sales/{sale_id}",
        headers={"Authorization": f"Bearer {invalid_access_token}"},
    )

    response_with_invalid_token = client.get(
        f"/v1/sales/{sale_id}",
        headers={"Authorization": f"Bearer {invalid_access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response_without_token.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_with_invalid_token.status_code == status.HTTP_401_UNAUTHORIZED
