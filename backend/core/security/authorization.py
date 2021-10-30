from datetime import timedelta
from typing import Union

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from pydantic import ValidationError

from backend.core.config import settings
from backend.core.helpers.date import now_datetime
from backend.core.helpers.exceptions import NotAuthorizedError
from backend.core.models import Token

ALGORITHM = "HS256"


def create_access_token(subject: str, expires_delta: Union[int, timedelta] = None) -> str:
    if not subject:
        raise ValueError("Subject can't be null")

    if expires_delta is None:
        expires_delta = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    if isinstance(expires_delta, int):
        expires_delta = timedelta(expires_delta)

    expire = now_datetime() + expires_delta

    to_encode = {"exp": expire, "sub": subject}

    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return token


def load_jwt_token(token: str) -> Token:
    try:
        return Token(**jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM]))

    except ExpiredSignatureError:
        raise NotAuthorizedError("Session expired!")

    except (jwt.JWTError, ValidationError):
        raise NotAuthorizedError("Couldn't possible load credentials!")
