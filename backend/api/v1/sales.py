from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.core import controller
from backend.core.helpers.database import Session, make_session
from backend.core.models import GetAllSales, SaleResponse

router = APIRouter()


@router.get("/", response_model=List[SaleResponse])
async def get_sales(query: GetAllSales = Depends(), session: Session = Depends(make_session)):
    return controller.sale.get_all(session, query)
