from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.services.inventory_service import create_inventory


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(
        name=data.name,
        sku=data.sku,
        category=data.category,
        purchase_price=data.purchase_price,
        selling_price=data.selling_price,
        supplier=data.supplier
    )

    try:
        db.add(product)
        db.flush()

        create_inventory(db, product.id, data.initial_quantity)

        db.commit()
        db.refresh(product)
        return product

    except IntegrityError:
        db.rollback()
        raise ValueError("SKU already exists")

    except Exception:
        db.rollback()
        raise


def get_products(db: Session):
    return db.query(Product).all()