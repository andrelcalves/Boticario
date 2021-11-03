from backend.core.helpers.documents import normalize_and_validate_cpf, normalize_cpf


def test_normalize_cpf_success():
    # Prepare
    cpf = "153.509.460-56"

    # Normalize
    normalized_cpf = normalize_cpf(cpf)

    # Assert
    assert normalized_cpf == "15350946056"


def test_normalize_and_validate_cpf_success():
    # Prepare
    cpf = "153.509.460-56"

    # Normalize
    result, normalized_cpf = normalize_and_validate_cpf(cpf)

    # Assert
    assert result is True
    assert normalized_cpf == "15350946056"


def test_normalize_and_validate_cpf_fail():
    # Prepare
    cpf = "153.509.460"

    # Normalize
    result, normalized_cpf = normalize_and_validate_cpf(cpf)

    # Assert
    assert result is False
    assert normalized_cpf is None
