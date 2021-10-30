from uuid import UUID

from sqlmodel import Field, SQLModel


class GetToken(SQLModel):
    cpf: str
    password: str


class Token(SQLModel):
    sub: UUID = Field(..., description="Seller ID")
    exp: int = Field(..., description="Timestamp that expire authentication")
