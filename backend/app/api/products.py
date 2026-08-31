from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.models.user import User
from app.services.product_service import product_service
from app.services.audit_service import audit_service
from app.utils.constants import AuditAction
from app.api.deps import get_current_user
from app.utils.helpers import PaginatedResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, summary="Create a product")
def create_product(
    product_in: ProductCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new product in the catalog."""
    product = product_service.create_product(db, product_in)
    client_ip = request.client.host if request.client else None
    audit_service.log_event(
        db=db,
        action=AuditAction.PRODUCT_CREATE,
        user_id=current_user.id,
        entity_type="Product",
        entity_id=str(product.id),
        ip_address=client_ip,
        metadata={"product_name": product.product_name, "category": product.category},
    )
    return product


@router.get("", response_model=PaginatedResponse[ProductResponse], summary="List products with pagination")
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get paginated list of catalog products."""
    skip = (page - 1) * limit
    items, total = product_service.list_products(db, skip=skip, limit=limit)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return PaginatedResponse[ProductResponse](
        items=[ProductResponse.model_validate(p) for p in items],
        page=page,
        limit=limit,
        total=total,
        total_pages=total_pages,
    )


@router.get("/search", response_model=List[ProductResponse], summary="Search products")
def search_products(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search products by name, brand, category, or manufacturer."""
    products = product_service.search_products(db, query_str=q, limit=limit)
    return [ProductResponse.model_validate(p) for p in products]


@router.get("/{product_id}", response_model=ProductResponse, summary="Get product by ID")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve product specifications by ID."""
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "PRODUCT_NOT_FOUND", "message": "Product not found."},
        )
    return product
