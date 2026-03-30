from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction


def create_inventory(db: Session, product_id: int, quantity: int):
    inventory = Inventory(product_id=product_id, quantity=quantity)
    db.add(inventory)
    db.refresh(inventory)
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