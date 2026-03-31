from pydantic import BaseModel, Field, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)


class StockReportResponse(BaseModel):
    product_name: str
    sku: str
    initial_stock: int
    quantity_sold: int
    current_stock: int

    model_config = ConfigDict(from_attributes=True)