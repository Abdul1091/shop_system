from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.services.inventory_service import update_inventory
from app.schemas.sale import SaleCreate
from fastapi import HTTPException


def create_sale(db: Session, user_id: int, sale_data: SaleCreate) -> Sale:
    """
    Creates a new sale with its items and updates inventory.
    Transaction is atomic: rollback on any error.
    """
    total_amount = 0
    new_sale = Sale(
        user_id=user_id,
        payment_method=sale_data.payment_method,
        total_amount=0  # temporary, will update later
    )

    try:
        # Process items and calculate total
        for item_data in sale_data.items:
            if item_data.quantity <= 0:
                raise HTTPException(status_code=400, detail=f"Quantity must be > 0 for product {item_data.product_id}")

            product = db.query(Product).filter_by(id=item_data.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product ID {item_data.product_id} not found")

            item_price = product.selling_price
            total_amount += item_price * item_data.quantity

            sale_item = SaleItem(
                product_id=product.id,
                quantity=item_data.quantity,
                price=item_price
            )
            new_sale.items.append(sale_item)

            # Deduct inventory safely
            update_inventory(
                db,
                product_id=product.id,
                change=-item_data.quantity,
                action_type="sale"
            )

        new_sale.total_amount = total_amount

        # Add and commit sale + items
        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)

        return new_sale

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

def get_detailed_sales_report(db: Session):
    # We join SaleItem -> Sale -> User and SaleItem -> Product
    results = (
        db.query(
            User.name.label("cashier_name"),
            Product.name.label("product_name"),
            SaleItem.quantity,
            SaleItem.price.label("price_per_unit"),
            (SaleItem.quantity * SaleItem.price).label("total_price"),
            Sale.created_at.label("timestamp")
        )
        .join(Sale, SaleItem.sale_id == Sale.id)
        .join(User, Sale.user_id == User.id)
        .join(Product, SaleItem.product_id == Product.id)
        .order_by(Sale.created_at.desc())
        .all()
    )
    return results