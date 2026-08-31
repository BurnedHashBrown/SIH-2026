from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.inspection import AnalysisResponse
from app.schemas.violation import (
    InspectorReviewCreate,
    InspectorReviewResponse,
    ViolationResponse,
    ViolationEvidenceResponse,
)
from app.schemas.image import BoundingBox
from app.models.user import User
from app.models.violation import Violation
from app.models.inspector_review import InspectorReview
from app.models.image import InspectionImage
from app.models.declaration import Declaration
from app.services.analysis_service import analysis_service
from app.services.audit_service import audit_service
from app.utils.constants import ViolationStatus, ReviewDecision, AuditAction
from app.api.deps import get_current_user

router = APIRouter(tags=["Analysis & Review"])


@router.post(
    "/inspections/{inspection_id}/analyze",
    response_model=AnalysisResponse,
    summary="Trigger full AI compliance analysis",
)
def run_inspection_analysis(
    inspection_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Executes OpenCV preprocessing, OCR detection, declaration extraction,
    rule engine evaluation, and preliminary compliance scoring.
    """
    return analysis_service.run_full_analysis(db, inspection_id, user_id=current_user.id)


@router.post(
    "/violations/{violation_id}/review",
    response_model=InspectorReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit inspector verification for potential violation",
)
def review_violation(
    violation_id: int,
    review_in: InspectorReviewCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Inspector confirms, rejects, edits, or marks as not applicable an AI finding.
    Preserves original AI prediction alongside inspector decision for full auditability.
    """
    violation = db.query(Violation).filter(Violation.id == violation_id).first()
    if not violation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "VIOLATION_NOT_FOUND", "message": "Violation record not found."},
        )

    # Record Review
    review = InspectorReview(
        violation_id=violation.id,
        inspector_id=current_user.id,
        decision=review_in.decision,
        remarks=review_in.remarks,
    )
    db.add(review)

    # Update violation status according to inspector decision
    if review_in.decision == ReviewDecision.CONFIRM:
        violation.status = ViolationStatus.CONFIRMED
    elif review_in.decision == ReviewDecision.REJECT:
        violation.status = ViolationStatus.REJECTED
    elif review_in.decision == ReviewDecision.NOT_APPLICABLE:
        violation.status = ViolationStatus.NOT_APPLICABLE

    db.commit()
    db.refresh(review)

    client_ip = request.client.host if request.client else None
    audit_service.log_event(
        db=db,
        action=AuditAction.VIOLATION_REVIEW,
        user_id=current_user.id,
        entity_type="Violation",
        entity_id=str(violation.id),
        ip_address=client_ip,
        metadata={
            "inspection_id": violation.inspection_id,
            "decision": review_in.decision.value,
            "remarks": review_in.remarks,
        },
    )

    return review


@router.get(
    "/violations/{violation_id}/evidence",
    response_model=ViolationEvidenceResponse,
    summary="Get visual evidence and bounding box for a violation",
)
def get_violation_evidence(
    violation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns image location and bounding coordinates corresponding to a flagged issue."""
    violation = db.query(Violation).filter(Violation.id == violation_id).first()
    if not violation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "VIOLATION_NOT_FOUND", "message": "Violation record not found."},
        )

    image = None
    if violation.evidence_image_id:
        image = db.query(InspectionImage).filter(InspectionImage.id == violation.evidence_image_id).first()

    bbox = None
    if violation.declaration:
        d = violation.declaration
        if d.bbox_x is not None:
            bbox = BoundingBox(
                x=d.bbox_x,
                y=d.bbox_y or 0.0,
                width=d.bbox_width or 0.0,
                height=d.bbox_height or 0.0,
            )

    return ViolationEvidenceResponse(
        violation_id=violation.id,
        image_id=image.id if image else None,
        image_url=image.storage_url if image else None,
        panel_type=image.panel_type.value if image else None,
        bbox=bbox,
        description=violation.description,
    )
