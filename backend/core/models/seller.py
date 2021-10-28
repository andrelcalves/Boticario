from uuid import uuid4, UUID
from pydantic.networks import EmailStr
from sqlmodel import SQLModel, Field
from backend.core.helpers.documents import normalize_and_validate_cpf
from pydantic import validator


class BaseSeller(SQLModel):
    cpf: str = Field(sa_column_args={"unique": True})
    name: str
    email: EmailStr

    @validator("cpf")
    def validate_cpf(cls, value: str) -> str:
        is_valid, normalized_value = normalize_and_validate_cpf(value)

        if not is_valid:
            raise ValueError(f'Cpf "{normalized_value}" is not valid!')

        return normalized_value


class CreateSeller(BaseSeller):
    password: str
    confirm_password: str


class Seller(BaseSeller):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password_hash: str
