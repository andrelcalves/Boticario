from typing import List
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.param_functions import Depends

from backend.core import controller
from backend.core.helpers.database import Session, make_session
from backend.core.models import CreateSale, GetAllSales, Sale, SaleResponse, Seller
from backend.core.models.sale import UpdateSale
from backend.dependencies import get_current_seller

router = APIRouter()


@router.get("/", response_model=List[SaleResponse])
async def get_all_sales(
    query: GetAllSales = Depends(),
    session: Session = Depends(make_session),
    current_seller: Seller = Depends(get_current_seller),
):
    query.seller_cpf = current_seller.cpf
    return controller.sale.get_all(session, query)


@router.post("/", response_model=Sale, status_code=status.HTTP_201_CREATED)
async def create_sale(
    schema: CreateSale, session: Session = Depends(make_session), current_seller: Seller = Depends(get_current_seller)
):
    return controller.sale.create(session, schema, current_seller)


@router.patch("/", response_model=Sale)
async def update_sale(
    schema: UpdateSale, session: Session = Depends(make_session), current_seller: Seller = Depends(get_current_seller)
):
    return controller.sale.update_sale_status_by_id(session, schema.id, schema.status, current_seller)


@router.get("/{sale_id}", response_model=Sale)
async def get_sale(sale_id: UUID, session: Session = Depends(make_session)):
    return controller.sale.get_by_id(session, sale_id)


@router.delete("/{sale_id}", response_model=Sale)
async def delete_sale(
    sale_id: UUID, session: Session = Depends(make_session), current_seller: Seller = Depends(get_current_seller)
):
    return controller.sale.delete_by_id(session, sale_id, current_seller)
