import datetime as dt
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import PositiveFloat, root_validator, validator
from sqlmodel import Column, Enum, Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from backend.core import controller
from backend.core.helpers.constants import SalesCashbackRange, SaleStatusEnum
from backend.core.helpers.database import session_context
from backend.core.helpers.documents import normalize_cpf

from .seller import Seller


class BaseSale(SQLModel):
    value: PositiveFloat
    item_code: str
    date: dt.date


class GetAllSales(SQLModel):
    seller_cpf: Optional[str]
    month: Optional[int]
    year: Optional[int]

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
    status: SaleStatusEnum = Field(default=SaleStatusEnum.PENDING)


class UpdateSale(SQLModel):
    id: UUID
    status: Optional[SaleStatusEnum]
    seller_cpf: Optional[str]
    value: Optional[float]
    item_code: Optional[str]
    date: Optional[dt.date]


class Sale(BaseSale, table=True):
    __tablename__ = "sales"

    id: UUID = Field(default_factory=uuid4, sa_column=Column("id", GUID(), primary_key=True))
    seller_cpf: str = Field(foreign_key="sellers.cpf")
    status: SaleStatusEnum = Field(sa_column=Column(Enum(SaleStatusEnum), nullable=False))

    seller: "Seller" = Relationship(back_populates="sales")

    @property
    def cashback_value(self) -> PositiveFloat:
        return self.value * self.cashback_percentual

    @property
    def cashback_percentual(self) -> PositiveFloat:
        with session_context() as session:
            total_sales = controller.sale.get_total_of_sales_by_period(
                session, self.seller.id, month=self.date.month, year=self.date.year
            )

        return SalesCashbackRange.get_percentual_by_total_value(total_sales)


class SaleResponse(BaseSale):
    id: UUID
    status: SaleStatusEnum
    cashback_value: PositiveFloat
    cashback_percentual: PositiveFloat
