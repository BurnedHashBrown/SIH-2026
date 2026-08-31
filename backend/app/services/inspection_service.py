from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from fastapi import HTTPException, status

from app.models.inspection import Inspection
from app.models.product import Product
from app.models.image import InspectionImage
from app.models.declaration import Declaration
from app.models.violation import Violation
from app.schemas.inspection import InspectionCreate, InspectionUpdate
from app.utils.constants import InspectionStatus
from app.utils.helpers import generate_inspection_id


class InspectionService:
    @staticmethod
    def get_inspection_by_id(db: Session, identifier: str | int) -> Optional[Inspection]:
        """Fetch inspection by numeric primary key or string inspection_id (e.g. LM-2026-0248)."""
        query = (
            db.query(Inspection)
            .options(
                joinedload(Inspection.product),
                joinedload(Inspection.images),
                joinedload(Inspection.declarations),
                joinedload(Inspection.violations).joinedload(Violation.reviews),
                joinedload(Inspection.violations).joinedload(Violation.rule),
                joinedload(Inspection.violations).joinedload(Violation.evidence_image),
                joinedload(Inspection.reports),
            )
        )
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            return query.filter(Inspection.id == int(identifier)).first()
        return query.filter(Inspection.inspection_id == str(identifier)).first()

    @staticmethod
    def create_inspection(db: Session, data: InspectionCreate, inspector_id: int) -> Inspection:
        # 1. Create or match Product
        product = (
            db.query(Product)
            .filter(
                Product.product_name == data.product_name,
                Product.batch_number == data.batch_number,
            )
            .first()
        )
        if not product:
            product = Product(
                product_name=data.product_name,
                brand=data.brand,
                category=data.category,
                manufacturer=data.manufacturer,
                packer=data.packer,
                importer=data.importer,
                batch_number=data.batch_number,
            )
            db.add(product)
            db.commit()
            db.refresh(product)

        # 2. Generate unique Inspection ID
        inspection_id = generate_inspection_id()
        while db.query(Inspection).filter(Inspection.inspection_id == inspection_id).first():
            inspection_id = generate_inspection_id()

        # 3. Create Inspection record
        inspection = Inspection(
            inspection_id=inspection_id,
            product_id=product.id,
            inspector_id=inspector_id,
            location=data.location or "Field Inspection",
            inspection_date=datetime.now(timezone.utc),
            status=InspectionStatus.DRAFT,
            compliance_score=0.0,
            total_checks=0,
            passed_checks=0,
            review_count=0,
            violation_count=0,
        )
        db.add(inspection)
        db.commit()
        db.refresh(inspection)
        return inspection

    @staticmethod
    def update_inspection(db: Session, inspection_id: str | int, update_data: InspectionUpdate) -> Inspection:
        inspection = InspectionService.get_inspection_by_id(db, inspection_id)
        if not inspection:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "INSPECTION_NOT_FOUND", "message": "Inspection not found."},
            )

        if update_data.location is not None:
            inspection.location = update_data.location
        if update_data.status is not None:
            inspection.status = update_data.status

        db.commit()
        db.refresh(inspection)
        return inspection

    @staticmethod
    def list_inspections(
        db: Session,
        search: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[InspectionStatus] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        inspector_id: Optional[int] = None,
        location: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> Tuple[List[Inspection], int]:
        query = db.query(Inspection).join(Product, Inspection.product_id == Product.id)

        filters = []
        if search:
            search_pat = f"%{search}%"
            filters.append(
                or_(
                    Inspection.inspection_id.ilike(search_pat),
                    Product.product_name.ilike(search_pat),
                    Product.brand.ilike(search_pat),
                    Product.manufacturer.ilike(search_pat),
                    Inspection.location.ilike(search_pat),
                )
            )
        if category:
            filters.append(Product.category.ilike(f"%{category}%"))
        if status:
            filters.append(Inspection.status == status)
        if date_from:
            filters.append(Inspection.inspection_date >= date_from)
        if date_to:
            filters.append(Inspection.inspection_date <= date_to)
        if inspector_id:
            filters.append(Inspection.inspector_id == inspector_id)
        if location:
            filters.append(Inspection.location.ilike(f"%{location}%"))

        if filters:
            query = query.filter(and_(*filters))

        total = query.count()
        offset = (page - 1) * limit
        items = (
            query.options(joinedload(Inspection.product))
            .order_by(Inspection.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return items, total


inspection_service = InspectionService()
