from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer

from backend.core.models import Authorization, Seller

from .core import controller
from .core.helpers.database import Session, make_session
from .core.helpers.exceptions import NotAuthorizedError, NotFoundError
from .core.security.authorization import load_authorization

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token/")


async def get_authorization(token: str = Depends(oauth2_scheme)) -> Authorization:
    return load_authorization(token)


async def get_current_seller(
    session: Session = Depends(make_session), auth: str = Depends(get_authorization)
) -> Seller:
    try:
        seller = controller.seller.get_by_id(session, auth.sub)

    except NotFoundError:
        raise NotAuthorizedError("Invalid authentication credentials")

    return seller


async def check_authorization(session: Session = Depends(make_session), auth: str = Depends(get_authorization)) -> None:
    if not controller.seller.check_if_exists(session, auth.sub):
        raise NotAuthorizedError("Invalid authentication credentials")
