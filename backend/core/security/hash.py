from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def check_password_hash(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)
