from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop Management System")

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "API is running"}