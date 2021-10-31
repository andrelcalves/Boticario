from backend.core.security.hash import check_password_hash, get_password_hash


def test_get_password_hash_success():
    password = "secret"

    password_hash = get_password_hash(password)

    assert password_hash is not None
    assert password_hash != password


def test_check_password_hash_success():
    password = "secret"
    password_hash = get_password_hash(password)

    assert check_password_hash(password, password_hash)


def test_check_password_hash_fail():
    password_hash = get_password_hash("secret")
    assert not check_password_hash("invalid_password", password_hash)
