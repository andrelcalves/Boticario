from uuid import UUID

from pydantic.types import PositiveFloat
from sqlmodel import Field, SQLModel


class SellerCashback(SQLModel):
    seller_id: UUID = Field(..., description="ID of the Seller")
    seller_cpf: str = Field(..., description="CPF of the Seller")
    seller_name: str = Field(..., description="Name of the Seller")
    total_cashback: PositiveFloat = Field(..., description="Total of the cashback acumulated")


class SaleCashback(SQLModel):
    sale_id: UUID = Field(..., description="ID of the Sale")
    cashback_value: PositiveFloat = Field(..., description="Value of the sale cashback")
    cashback_percentual: PositiveFloat = Field(..., description="Percentual of the sale cashback")
