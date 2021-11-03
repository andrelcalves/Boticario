import pytest

from backend.core.helpers.exceptions import DatabaseError, NotAuthorizedError, NotFoundError, ServiceError


def test_not_authorized_error():
    # Prepare
    message = "Invalid credentials"

    # Create
    exc = NotAuthorizedError(message)

    # Assert
    assert exc.detail == message
    assert issubclass(NotAuthorizedError, Exception)

    with pytest.raises(NotAuthorizedError):
        raise exc


def test_database_error():
    # Prepare
    message = "Error in the database!"

    # Create
    exc = DatabaseError(message)

    # Assert
    assert exc.detail == message
    assert issubclass(DatabaseError, Exception)

    with pytest.raises(DatabaseError):
        raise exc


def test_notfound_error():
    # Prepare
    message = "Couldn't found current data"

    # Create
    exc = NotFoundError(message)

    # Assert
    assert exc.detail == message
    assert issubclass(NotFoundError, Exception)

    with pytest.raises(NotFoundError):
        raise exc


def test_service_error():
    # Prepare
    service = "I'm a fake test service"
    message = "Testing the service error"

    # Create
    exc = ServiceError(service, message)

    # Assert
    assert issubclass(ServiceError, Exception)
    assert exc.service == service
    assert exc.detail == message

    with pytest.raises(ServiceError):
        raise exc
