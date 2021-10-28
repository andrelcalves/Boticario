from typing import Tuple, Union
from validate_docbr import CPF

_cpf_validator = CPF()


def normalize_cpf(cpf: str) -> str:
    return "".join([x for x in cpf if x.isdigit()])


def normalize_and_validate_cpf(cpf: str) -> Tuple[bool, Union[str, None]]:
    normalized_cpf = normalize_cpf(cpf)

    return _cpf_validator.validate(normalized_cpf), normalized_cpf
