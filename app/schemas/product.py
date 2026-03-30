from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    sku: str
    category: str | None = None
    purchase_price: float
    selling_price: float
    supplier: str | None = None
    initial_quantity: int = 0


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    selling_price: float

    class Config:
        from_attributes = True