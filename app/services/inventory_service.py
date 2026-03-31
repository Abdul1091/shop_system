from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.inventory_transaction import InventoryTransaction


def create_inventory(db: Session, product_id: int, quantity: int):
    inventory = Inventory(product_id=product_id, quantity=quantity)
    db.add(inventory)
    # db.refresh(inventory)
    return inventory


def update_inventory(db: Session, product_id: int, change: int, action_type: str):
    inventory = db.query(Inventory).filter_by(product_id=product_id).first()

    if not inventory:
        raise Exception("Inventory not found")

    new_quantity = inventory.quantity + change

    if new_quantity < 0:
        raise Exception("Insufficient stock")

    inventory.quantity = new_quantity

    transaction = InventoryTransaction(
        product_id=product_id,
        change=change,
        type=action_type
    )

    db.add(transaction)
    return inventory


def get_stock_report(db: Session):
    products = db.query(Product).all()
    report = []

    for product in products:
        # 1. Get current stock from Inventory table
        current_inventory = db.query(Inventory).filter_by(product_id=product.id).first()
        current_stock = current_inventory.quantity if current_inventory else 0

        # 2. Calculate Total Sold from Transactions
        # We sum the absolute value of 'change' where type is 'sale'
        sold_data = db.query(func.sum(InventoryTransaction.change)).filter(
            InventoryTransaction.product_id == product.id,
            InventoryTransaction.type == "sale"
        ).scalar() or 0
        
        quantity_sold = abs(sold_data)

        # 3. Calculate Initial Stock (Remaining + Sold)
        initial_stock = current_stock + quantity_sold

        report.append({
            "product_name": product.name,
            "sku": product.sku,
            "initial_stock": initial_stock,
            "quantity_sold": quantity_sold,
            "current_stock": current_stock
        })
    
    return report