from sqlmodel import SQLModel
import datetime as dt


class BaseSale(SQLModel):
    saller_cpf: str
    value: float
    item_code: str
    date: dt.date


# Colocar Status
