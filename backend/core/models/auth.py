from uuid import UUID

from sqlmodel import Field, SQLModel


class Authorization(SQLModel):
    sub: UUID = Field(..., description="Seller ID")
    exp: int = Field(..., description="Timestamp that expire authentication")


class Token(SQLModel):
    access_token: str = Field(..., description="Encoded authorization token")
    token_type: str = Field(..., description="Type of token")
    expires: int = Field(..., description="Timestamp that expire authentication")
