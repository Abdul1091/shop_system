from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime
from app.database import Base


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    change = Column(Integer)  # +ve or -ve
    type = Column(String)  # "sale", "purchase", "adjustment"
    timestamp = Column(DateTime, default=datetime.utcnow)