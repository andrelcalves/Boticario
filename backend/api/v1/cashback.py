from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlmodel import Session

from backend.core import controller
from backend.core.helpers.database import make_session
from backend.core.models import CashbackResponse
from backend.core.services import CashbackClient, DefaultCashbackClient

router = APIRouter()


@router.get("/{seller_id}", response_model=CashbackResponse)
async def get_total_cashback_by_seller_id(
    seller_id: UUID,
    session: Session = Depends(make_session),
    cashback_client: CashbackClient = Depends(DefaultCashbackClient),
):
    seller = controller.seller.get_by_id(session, seller_id)
    total_cashback = cashback_client.get_total(seller.cpf)

    data = {
        "seller_id": seller.id,
        "seller_name": seller.name,
        "seller_cpf": seller.cpf,
        "total_cashback": total_cashback,
    }

    return data
