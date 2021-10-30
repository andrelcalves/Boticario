from fastapi import APIRouter

from . import sales, seller

endpoints = APIRouter()

endpoints.include_router(seller.router, prefix="/seller", tags=["Seller"])
endpoints.include_router(sales.router, prefix="/sales", tags=["Sales"])
