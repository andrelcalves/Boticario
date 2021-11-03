from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.core import controller, models
from tests.factories.seller import CreateSellerFactory


def test_get_total_cashback_by_seller_id_success(client: TestClient, session: Session):
    # Prepare
    schema = CreateSellerFactory()
    seller = controller.seller.create(session, schema)

    auth_response = client.post("/auth/token", data={"username": schema.cpf, "password": schema.password})
    auth_data = auth_response.json()

    # Request
    response = client.get(
        f"/v1/cashback/{seller.id}",
        headers={"Authorization": f"Bearer {auth_data['access_token']}"},
    )
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert models.SellerCashback.validate(data)
