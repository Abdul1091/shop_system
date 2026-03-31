from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth_routes, product_routes, sales_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop Management System")

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(sales_routes.router, prefix="/sales", tags=["Sales"])