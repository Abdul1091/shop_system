from pydantic import BaseModel
from typing import List
from datetime import datetime


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int


class SaleCreate(BaseModel):
    items: List[SaleItemCreate]
    payment_method: str


class SaleItemRead(BaseModel):
    product_id: int
    quantity: int
    price: float
    
    class Config:
        from_attributes = True


class SaleResponse(BaseModel):
    id: int
    total_amount: float
    payment_method: str
    created_at: datetime
    items: List[SaleItemRead]

    class Config:
        from_attributes = True