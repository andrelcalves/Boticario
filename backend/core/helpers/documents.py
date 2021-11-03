from typing import Tuple, Union

from validate_docbr import CPF

_cpf_validator = CPF()


def normalize_cpf(cpf: str) -> str:
    return "".join([x for x in cpf if x.isdigit()])


def normalize_and_validate_cpf(cpf: str) -> Tuple[bool, Union[str, None]]:
    cpf_is_valid = _cpf_validator.validate(cpf)

    if not cpf_is_valid:
        return cpf_is_valid, None

    return cpf_is_valid, normalize_cpf(cpf)
