from fastapi import APIRouter

from . import cashback, sales, seller

endpoints = APIRouter()

endpoints.include_router(seller.router, prefix="/seller", tags=["Seller"])
endpoints.include_router(sales.router, prefix="/sales", tags=["Sales"])
endpoints.include_router(cashback.router, prefix="/cashback", tags=["Cashback"])
