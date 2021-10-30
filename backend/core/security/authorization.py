from datetime import timedelta
from typing import Union
from uuid import UUID

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from pydantic import ValidationError

from backend.core.config import settings
from backend.core.helpers.date import now_datetime
from backend.core.helpers.exceptions import NotAuthorizedError
from backend.core.models import Authorization, Token

ALGORITHM = "HS256"


def create_access_token(subject: UUID, expires_delta: Union[int, timedelta] = None) -> Token:
    if not subject:
        raise ValueError("Subject can't be null")

    if expires_delta is None:
        expires_delta = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    if isinstance(expires_delta, int):
        expires_delta = timedelta(expires_delta)

    expire = now_datetime() + expires_delta

    to_encode = {"exp": expire, "sub": str(subject)}

    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return Token(access_token=token, token_type="bearer", expires=expire.timestamp())


def load_authorization(token: str) -> Authorization:
    try:
        return Authorization(**jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM]))

    except ExpiredSignatureError:
        raise NotAuthorizedError("Session expired!")

    except (jwt.JWTError, ValidationError):
        raise NotAuthorizedError("Couldn't possible load credentials!")
