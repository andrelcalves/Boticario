from typing import TYPE_CHECKING, Any, Dict, List
from uuid import UUID, uuid4

from pydantic import validator
from pydantic.networks import EmailStr
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from backend.core.helpers.documents import normalize_and_validate_cpf

if TYPE_CHECKING:
    from .sale import Sale, SaleResponse


class BaseSeller(SQLModel):
    cpf: str = Field(..., description="CPF of the Seller", sa_column_kwargs={"unique": True})
    name: str = Field(..., description="Name of the Seller")
    email: EmailStr = Field(..., description="Email of the Seller")

    @validator("name")
    def validate_name(cls, value: str) -> str:
        if len(value.split(" ")) < 2:
            raise ValueError("Name and lastname is required!")

        if any(x.isdigit() for x in value):
            raise ValueError("Name couldn't contains numeric characters")

        return value

    @validator("cpf")
    def validate_cpf(cls, value: str) -> str:
        is_valid, normalized_value = normalize_and_validate_cpf(value)

        if not is_valid:
            raise ValueError(f'Cpf "{normalized_value}" is not valid!')

        return normalized_value


class CreateSeller(BaseSeller):
    password: str = Field(..., description="Password")
    confirm_password: str = Field(..., description="Confirmation of the password")

    @validator("confirm_password")
    def check_password(cls, value: str, values: Dict[str, Any]) -> str:
        if value != values.get("password"):
            raise ValueError("The password and confirmation must be equal!")

        return value


class Seller(BaseSeller, table=True):
    __tablename__ = "sellers"

    id: UUID = Field(
        default_factory=uuid4, description="ID of the Seller", sa_column=Column("id", GUID(), primary_key=True)
    )
    password_hash: str = Field(..., description="Hash of Seller password")

    sales: List["Sale"] = Relationship(back_populates="seller")


class SellerResponse(BaseSeller):
    id: UUID = Field(..., description="ID of the Seller")

    sales: List["SaleResponse"]
