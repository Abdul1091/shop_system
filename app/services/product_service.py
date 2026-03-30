from sqlalchemy.orm import Session
from app.models.product import Product
from app.services.inventory_service import create_inventory


def create_product(db: Session, data):
    product = Product(
        name=data.name,
        sku=data.sku,
        category=data.category,
        purchase_price=data.purchase_price,
        selling_price=data.selling_price,
        supplier=data.supplier
    )

    db.add(product)
    db.flush()  # get product.id BEFORE commit

    create_inventory(db, product.id, data.initial_quantity)

    db.commit()
    db.refresh(product)

    return product


def get_products(db: Session):
    return db.query(Product).all()