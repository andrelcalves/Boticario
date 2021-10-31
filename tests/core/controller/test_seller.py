from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlmodel import Session

from backend.core import controller
from backend.core.helpers.exceptions import DatabaseError, NotFoundError
from tests.factories.seller import CreateSellerFactory


def test_create_success(session: Session):
    # Prepare
    schema = CreateSellerFactory()

    # Create
    seller = controller.seller.create(session, schema)

    # Assert
    assert seller is not None
    assert seller.name == schema.name
    assert seller.cpf == schema.cpf
    assert seller.id is not None
    assert seller.password_hash != schema.password


def test_create_fail(session: Session):
    # Prepare
    schema = CreateSellerFactory()
    schema2 = CreateSellerFactory(cpf=schema.cpf)

    # Create
    controller.seller.create(session, schema)

    # assert
    with pytest.raises(DatabaseError):
        controller.seller.create(session, schema2)

    with pytest.raises(ValidationError):
        CreateSellerFactory(name=None)

    with pytest.raises(ValidationError):
        CreateSellerFactory(cpf=None)

    with pytest.raises(ValidationError):
        CreateSellerFactory(password=None)


def test_create_without_last_name_fail(session: Session):
    with pytest.raises(ValidationError):
        CreateSellerFactory(name="Name")


def test_create_with_numbers(session: Session):
    with pytest.raises(ValidationError):
        CreateSellerFactory(name="Name123 lastname")


def test_get_by_cpf_success(session: Session):
    # Prepare
    schema = CreateSellerFactory()

    # Create
    seller = controller.seller.create(session, schema)
    seller2 = controller.seller.get_by_cpf(session, schema.cpf)

    # assert
    assert seller2 is not None
    assert seller.cpf == seller2.cpf
    assert seller == seller2


def test_get_by_cpf_fail(session: Session):
    with pytest.raises(NotFoundError):
        controller.seller.get_by_cpf(session, "12345678900")


def test_get_by_id_success(session: Session):
    # Prepare
    schema = CreateSellerFactory()

    # Create
    seller = controller.seller.create(session, schema)
    seller2 = controller.seller.get_by_id(session, seller.id)

    # assert
    assert seller2 is not None
    assert seller.id == seller2.id
    assert seller == seller2


def test_get_by_id_fail(session: Session):
    with pytest.raises(NotFoundError):
        controller.seller.get_by_id(session, uuid4())


def test_check_if_exists_success(session: Session):
    # Prepare
    schema = CreateSellerFactory()

    # Create
    seller = controller.seller.create(session, schema)

    # Assert
    assert controller.seller.check_if_exists(session, seller.id) is True


def test_check_if_exists_fail(session: Session):
    assert controller.seller.check_if_exists(session, uuid4()) is False
