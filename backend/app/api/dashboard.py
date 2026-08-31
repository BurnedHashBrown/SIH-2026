from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    DashboardViolationsResponse,
    RecentInspectionItem,
)
from app.models.inspection import Inspection
from app.models.violation import Violation
from app.models.declaration import Declaration
from app.models.product import Product
from app.models.user import User
from app.utils.constants import InspectionStatus, DeclarationType
from app.api.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse, summary="Get dashboard inspection summary counts")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns aggregated high-level inspection statistics."""
    total = db.query(Inspection).count()
    compliant = db.query(Inspection).filter(Inspection.status == InspectionStatus.COMPLIANT).count()
    potential = (
        db.query(Inspection)
        .filter(Inspection.status.in_([InspectionStatus.POTENTIAL_NON_COMPLIANCE, InspectionStatus.ANALYSIS_COMPLETE]))
        .count()
    )
    review = db.query(Inspection).filter(Inspection.status == InspectionStatus.REQUIRES_REVIEW).count()

    return DashboardSummaryResponse(
        total_inspections=total,
        compliant=compliant,
        potential_violations=potential,
        requires_review=review,
    )


@router.get("/violations", response_model=DashboardViolationsResponse, summary="Get violation breakdown by category")
def get_dashboard_violations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns total frequency of violations and review items per declaration type."""
    # Query violations grouped by declaration type
    violations = (
        db.query(Declaration.type, func.count(Violation.id))
        .join(Violation, Violation.declaration_id == Declaration.id)
        .group_by(Declaration.type)
        .all()
    )

    counts = {decl_type.value: count for decl_type, count in violations}

    # Count violations without linked declaration or general readability
    readability_count = (
        db.query(Violation)
        .filter(Violation.description.ilike("%readability%") | Violation.description.ilike("%legib%"))
        .count()
    )

    return DashboardViolationsResponse(
        consumer_care=counts.get(DeclarationType.CONSUMER_CARE.value, 0),
        mrp=counts.get(DeclarationType.MRP.value, 0),
        net_quantity=counts.get(DeclarationType.NET_QUANTITY.value, 0),
        manufacturer=counts.get(DeclarationType.MANUFACTURER.value, 0),
        readability=readability_count,
        date_information=counts.get(DeclarationType.DATE_INFORMATION.value, 0),
        other=counts.get(DeclarationType.OTHER.value, 0),
    )


@router.get("/recent-inspections", response_model=List[RecentInspectionItem], summary="Get recent inspections")
def get_recent_inspections(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns most recent inspections for fast dashboard display."""
    inspections = (
        db.query(Inspection)
        .join(Product, Inspection.product_id == Product.id)
        .order_by(Inspection.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        RecentInspectionItem(
            id=insp.id,
            inspection_id=insp.inspection_id,
            product_name=insp.product.product_name if insp.product else "N/A",
            brand=insp.product.brand if insp.product else None,
            category=insp.product.category if insp.product else None,
            status=insp.status,
            compliance_score=insp.compliance_score,
            inspection_date=insp.inspection_date,
        )
        for insp in inspections
    ]
