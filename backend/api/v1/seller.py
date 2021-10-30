from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.core import controller
from backend.core.helpers.database import Session, make_session
from backend.core.models import Seller
from backend.core.models.seller import CreateSeller

router = APIRouter()


@router.post(
    "/", response_model=Seller, description="Register a new seller", response_model_exclude={"password_hash": ...}
)
async def create_seller(schema: CreateSeller, session: Session = Depends(make_session)):
    return controller.seller.create(session, schema)
