from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlmodel import Session

from backend.core import controller
from backend.core.helpers.database import make_session
from backend.core.models import SellerCashback

router = APIRouter()


@router.get("/{seller_id}", response_model=SellerCashback)
async def get_total_cashback_by_seller_id(
    seller_id: UUID,
    session: Session = Depends(make_session),
):
    return controller.cashback.get_seller_cashback_by_id(session, seller_id)
