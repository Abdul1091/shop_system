from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime, UTC
from app.database import Base
from sqlalchemy.orm import relationship


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    change = Column(Integer)  # +ve or -ve
    type = Column(String)  # "sale", "purchase", "adjustment"
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))

    product = relationship("Product", back_populates="transactions")