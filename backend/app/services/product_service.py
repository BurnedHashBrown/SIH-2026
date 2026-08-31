from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def create_product(db: Session, product_in: ProductCreate) -> Product:
        db_product = Product(
            product_name=product_in.product_name,
            brand=product_in.brand,
            category=product_in.category,
            manufacturer=product_in.manufacturer,
            packer=product_in.packer,
            importer=product_in.importer,
            batch_number=product_in.batch_number,
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Product:
        product = ProductService.get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "PRODUCT_NOT_FOUND", "message": "Product not found."},
            )

        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def list_products(db: Session, skip: int = 0, limit: int = 20) -> Tuple[List[Product], int]:
        query = db.query(Product)
        total = query.count()
        items = query.order_by(Product.created_at.desc()).offset(skip).limit(limit).all()
        return items, total

    @staticmethod
    def search_products(db: Session, query_str: str, limit: int = 20) -> List[Product]:
        search_pattern = f"%{query_str}%"
        return (
            db.query(Product)
            .filter(
                or_(
                    Product.product_name.ilike(search_pattern),
                    Product.brand.ilike(search_pattern),
                    Product.category.ilike(search_pattern),
                    Product.manufacturer.ilike(search_pattern),
                    Product.batch_number.ilike(search_pattern),
                )
            )
            .limit(limit)
            .all()
        )


product_service = ProductService()
