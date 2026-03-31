from pydantic import BaseModel, ConfigDict
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
    
    model_config = ConfigDict(from_attributes=True)


class SaleResponse(BaseModel):
    id: int
    total_amount: float
    payment_method: str
    created_at: datetime
    items: List[SaleItemRead]

    model_config = ConfigDict(from_attributes=True)


class DetailedSaleReport(BaseModel):
    cashier_name: str
    product_name: str
    quantity: int
    price_per_unit: float
    total_price: float
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)