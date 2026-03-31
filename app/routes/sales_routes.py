from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleResponse, DetailedSaleReport
from app.services.sales_service import create_sale, get_detailed_sales_report
from app.core.dependencies import require_roles


router = APIRouter()


@router.post("/", response_model=SaleResponse)
def create_new_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("owner", "cashier"))
):
    """
    Create a sale and deduct inventory. Only accessible by owners and cashiers.
    """
    return create_sale(db, user_id=user.id, sale_data=data)


@router.get("/detailed-report", response_model=List[DetailedSaleReport])
def view_detailed_sales(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("owner"))
):
    return get_detailed_sales_report(db)