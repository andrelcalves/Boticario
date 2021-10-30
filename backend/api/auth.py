from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.core import controller
from backend.core.helpers.database import Session, make_session
from backend.core.helpers.exceptions import NotAuthorizedError, NotFoundError
from backend.core.models import Token
from backend.core.security.authorization import create_access_token
from backend.core.security.hash import check_password_hash

router = APIRouter()


@router.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(make_session)):
    try:
        seller = controller.seller.get_by_cpf(session, form.username)

    except NotFoundError as err:
        raise NotAuthorizedError(err.detail)

    if not check_password_hash(form.password, seller.password_hash):
        raise NotAuthorizedError("Invalid password!")

    return create_access_token(seller.id)
