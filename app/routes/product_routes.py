from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, StockReportResponse
from app.services.product_service import create_product, get_products
from app.core.dependencies import require_roles
from app.services.inventory_service import get_stock_report

router = APIRouter()


@router.post("/", response_model=ProductResponse)
def create_new_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("owner"))
):
    try:
        return create_product(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("owner", "cashier"))
):
    
    return get_products(db)


@router.get("/report", response_model=List[StockReportResponse])
def view_stock_report(
    db: Session = Depends(get_db),
    user = Depends(require_roles("owner"))
):
    return get_stock_report(db)