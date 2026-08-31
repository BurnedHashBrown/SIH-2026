from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.inspection import (
    InspectionCreate,
    InspectionUpdate,
    InspectionResponse,
    InspectionDetailResponse,
)
from app.schemas.image import ImageUploadResponse, ImageResponse, BoundingBox
from app.models.user import User
from app.models.image import InspectionImage
from app.services.inspection_service import inspection_service
from app.services.storage_service import storage_service
from app.services.audit_service import audit_service
from app.ai.preprocessing import image_preprocessor
from app.utils.constants import InspectionStatus, PanelType, AuditAction
from app.api.deps import get_current_user
from app.utils.helpers import PaginatedResponse

router = APIRouter(prefix="/inspections", tags=["Inspections"])


@router.post("", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED, summary="Create a new inspection")
def create_inspection(
    inspection_in: InspectionCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new compliance inspection with product information."""
    inspection = inspection_service.create_inspection(db, inspection_in, inspector_id=current_user.id)
    client_ip = request.client.host if request.client else None
    audit_service.log_event(
        db=db,
        action=AuditAction.INSPECTION_CREATE,
        user_id=current_user.id,
        entity_type="Inspection",
        entity_id=str(inspection.id),
        ip_address=client_ip,
        metadata={"inspection_id": inspection.inspection_id, "product": inspection_in.product_name},
    )
    return inspection


@router.get("", response_model=PaginatedResponse[InspectionResponse], summary="List inspections with filtering and search")
def list_inspections(
    search: Optional[str] = Query(None, description="Search across inspection ID, product name, brand, location"),
    category: Optional[str] = Query(None, description="Filter by product category"),
    status: Optional[InspectionStatus] = Query(None, description="Filter by inspection status"),
    date_from: Optional[datetime] = Query(None, description="Filter inspections on or after this ISO date"),
    date_to: Optional[datetime] = Query(None, description="Filter inspections on or before this ISO date"),
    inspector_id: Optional[int] = Query(None, description="Filter by inspector ID"),
    location: Optional[str] = Query(None, description="Filter by location"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve paginated inspections with rich query criteria."""
    items, total = inspection_service.list_inspections(
        db=db,
        search=search,
        category=category,
        status=status,
        date_from=date_from,
        date_to=date_to,
        inspector_id=inspector_id,
        location=location,
        page=page,
        limit=limit,
    )
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return PaginatedResponse[InspectionResponse](
        items=[InspectionResponse.model_validate(item) for item in items],
        page=page,
        limit=limit,
        total=total,
        total_pages=total_pages,
    )


@router.get("/{inspection_id}", response_model=InspectionDetailResponse, summary="Get full inspection details")
def get_inspection(
    inspection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve complete inspection records, images, declarations, violations, and reports."""
    inspection = inspection_service.get_inspection_by_id(db, inspection_id)
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "INSPECTION_NOT_FOUND", "message": f"Inspection '{inspection_id}' not found."},
        )
    return inspection


@router.put("/{inspection_id}", response_model=InspectionResponse, summary="Update inspection details")
def update_inspection(
    inspection_id: str,
    update_data: InspectionUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update inspection status or field location."""
    updated = inspection_service.update_inspection(db, inspection_id, update_data)
    client_ip = request.client.host if request.client else None
    audit_service.log_event(
        db=db,
        action=AuditAction.INSPECTION_UPDATE,
        user_id=current_user.id,
        entity_type="Inspection",
        entity_id=str(updated.id),
        ip_address=client_ip,
        metadata={"inspection_id": updated.inspection_id, "new_status": updated.status.value},
    )
    return updated


# --- Image Upload & Inspection Images Sub-routes ---

@router.post(
    "/{inspection_id}/images",
    response_model=ImageUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload packaging image for an inspection",
)
async def upload_inspection_image(
    inspection_id: str,
    request: Request,
    file: UploadFile = File(...),
    panel_type: PanelType = Form(PanelType.FRONT),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload a packaging image, validate format/size/dimensions, assess quality with OpenCV."""
    inspection = inspection_service.get_inspection_by_id(db, inspection_id)
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "INSPECTION_NOT_FOUND", "message": f"Inspection '{inspection_id}' not found."},
        )

    # 1. Validate and store file
    safe_filename, file_path, width, height, raw_bytes = await storage_service.save_image(file)

    # 2. Run OpenCV Image Quality Check
    quality_result = image_preprocessor.assess_quality(file_path, raw_bytes)

    # 3. Store database record
    db_image = InspectionImage(
        inspection_id=inspection.id,
        file_name=safe_filename,
        storage_url=f"/uploads/{safe_filename}",
        panel_type=panel_type,
        image_quality_score=quality_result.quality_score,
        width=width,
        height=height,
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    # 4. Audit Log
    client_ip = request.client.host if request.client else None
    audit_service.log_event(
        db=db,
        action=AuditAction.IMAGE_UPLOAD,
        user_id=current_user.id,
        entity_type="InspectionImage",
        entity_id=str(db_image.id),
        ip_address=client_ip,
        metadata={
            "inspection_id": inspection.inspection_id,
            "panel_type": panel_type.value,
            "quality_score": quality_result.quality_score,
        },
    )

    return ImageUploadResponse(
        image_id=db_image.id,
        file_name=db_image.file_name,
        panel_type=db_image.panel_type,
        quality_score=db_image.image_quality_score,
        storage_url=db_image.storage_url,
        width=db_image.width,
        height=db_image.height,
        is_acceptable=quality_result.is_acceptable,
        warnings=quality_result.warnings,
    )


@router.get("/{inspection_id}/images", response_model=List[ImageResponse], summary="List images for an inspection")
def list_inspection_images(
    inspection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all packaging panel photos attached to an inspection."""
    inspection = inspection_service.get_inspection_by_id(db, inspection_id)
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "INSPECTION_NOT_FOUND", "message": f"Inspection '{inspection_id}' not found."},
        )
    return db.query(InspectionImage).filter(InspectionImage.inspection_id == inspection.id).all()
