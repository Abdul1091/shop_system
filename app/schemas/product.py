from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    sku: str
    category: str | None = None
    purchase_price: float = Field(gt=0)
    selling_price: float = Field(gt=0)
    supplier: str | None = None
    initial_quantity: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    selling_price: float
    category: str | None
    supplier: str | None

    class Config:
        from_attributes = True