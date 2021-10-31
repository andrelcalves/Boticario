from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.dependencies import check_authorization

from . import cashback, sales, seller

endpoints = APIRouter()

endpoints.include_router(seller.router, prefix="/seller", tags=["Seller"], dependencies=[Depends(check_authorization)])
endpoints.include_router(sales.router, prefix="/sales", tags=["Sales"], dependencies=[Depends(check_authorization)])
endpoints.include_router(
    cashback.router, prefix="/cashback", tags=["Cashback"], dependencies=[Depends(check_authorization)]
)
