from fastapi import APIRouter, status
from fastapi.param_functions import Depends

from backend.core import controller
from backend.core.helpers.database import Session, make_session
from backend.core.models import Seller
from backend.core.models.seller import CreateSeller
from backend.dependencies import get_current_seller

router = APIRouter()


@router.post(
    "/",
    response_model=Seller,
    status_code=status.HTTP_201_CREATED,
    description="Register a new seller",
    response_model_exclude={"password_hash": ...},
)
async def create_seller(
    schema: CreateSeller, session: Session = Depends(make_session), current_seller: Seller = Depends(get_current_seller)
):
    return controller.seller.create(session, schema)
