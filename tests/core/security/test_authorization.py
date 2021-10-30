from datetime import timedelta
from uuid import uuid4

import pytest

from backend.core.helpers.exceptions import NotAuthorizedError
from backend.core.security.authorization import create_access_token, load_jwt_token


def test_create_access_token_success():
    # Prepare
    subject = str(uuid4())

    # Create
    token = create_access_token(subject)

    # Assert
    assert token is not None
    assert load_jwt_token(token) is not None


def test_create_access_token_fail():
    with pytest.raises(ValueError):
        create_access_token(None)

    with pytest.raises(ValueError):
        create_access_token("")


def test_load_jwt_token_fail():
    with pytest.raises(NotAuthorizedError):
        load_jwt_token("")


def test_load_jwt_token_expired_fail():
    subject = str(uuid4())
    token = create_access_token(subject, timedelta(-1))

    with pytest.raises(NotAuthorizedError):
        load_jwt_token(token)
