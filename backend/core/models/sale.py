import datetime as dt
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import PositiveFloat, root_validator, validator
from sqlmodel import Column, Enum, Field, Relationship, SQLModel, extract, select
from sqlmodel.sql.sqltypes import GUID

from backend.core.helpers.constants import SalesCashbackRange, SaleStatusEnum
from backend.core.helpers.database import session_context
from backend.core.helpers.documents import normalize_cpf

from .seller import Seller


class BaseSale(SQLModel):
    value: PositiveFloat = Field(..., description="Value of the sale")
    item_code: str = Field(..., description="Code of the item")
    date: dt.date = Field(..., description="Date of the sale")


class GetAllSales(SQLModel):
    seller_cpf: Optional[str] = Field(..., description="CPF of the Seller who made the purchase")
    month: Optional[int] = Field(..., description="Month of the sale for the query *required if year is informed")
    year: Optional[int] = Field(..., description="Year of the sale for the query *required if month is informed")

    @root_validator()
    def validate_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values.get("month") is not None and values.get("year") is None:
            raise ValueError("If month is informed, year is required!")

        if values.get("year") is not None and values.get("month") is None:
            raise ValueError("If year is informed, month is required!")

        return values

    @validator("seller_cpf")
    def normalize_seller_cpf(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            return normalize_cpf(value)

        return value


class CreateSale(BaseSale):
    pass


class UpdateSale(SQLModel):
    id: UUID = Field(..., description="ID of the purchase")
    status: SaleStatusEnum = Field(
        description="New status of the purchase, it is only possible to change if status is pending"
    )


class Sale(BaseSale, table=True):
    __tablename__ = "sales"

    id: UUID = Field(
        default_factory=uuid4, description="ID of the purchase", sa_column=Column("id", GUID(), primary_key=True)
    )
    seller_cpf: str = Field(description="CPF of the Seller who made the purchase", foreign_key="sellers.cpf")
    status: SaleStatusEnum = Field(
        default=SaleStatusEnum.PENDING,
        description="Current Status of the purchase",
        sa_column=Column(Enum(SaleStatusEnum), nullable=False),
    )

    seller: "Seller" = Relationship(back_populates="sales")

    @property
    def cashback_value(self) -> PositiveFloat:
        return self.value * self.cashback_percentual

    @property
    def cashback_percentual(self) -> PositiveFloat:
        with session_context() as session:
            sales = session.exec(
                select(Sale)
                .join(Seller)
                .where(
                    Seller.id == self.seller.id,
                    extract("month", Sale.date) == self.date.month,
                    extract("year", Sale.date) == self.date.year,
                )
            ).all()

            total_sales = sum(s.value for s in sales)

        return SalesCashbackRange.get_percentual_by_total_value(total_sales)


class SaleResponse(BaseSale):
    id: UUID = Field(..., description="ID of the purchase", sa_column=Column("id", GUID(), primary_key=True))
    status: SaleStatusEnum = Field(..., description="Current Status of the purchase")
    cashback_value: PositiveFloat = Field(..., description="Value of the cashback for the sale")
    cashback_percentual: PositiveFloat = Field(..., description="Percentual of the cashback for the sale")
