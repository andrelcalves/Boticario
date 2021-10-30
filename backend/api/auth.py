from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.core import controller
from backend.core.helpers.database import Session, make_session
from backend.core.helpers.exceptions import NotAuthorizedError
from backend.core.models import GetToken
from backend.core.security.authorization import create_access_token
from backend.core.security.hash import check_password_hash

router = APIRouter()


@router.post("/token")
async def get_token(schema: GetToken, session: Session = Depends(make_session)):
    seller = controller.seller.get_by_cpf(session, schema.cpf)

    if not check_password_hash(schema.password, seller.password_hash):
        raise NotAuthorizedError("Invalid password!")

    return create_access_token(seller.id)
