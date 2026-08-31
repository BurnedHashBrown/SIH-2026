import os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.report import ReportResponse
from app.models.user import User
from app.models.report import Report
from app.services.report_service import report_service
from app.services.audit_service import audit_service
from app.utils.constants import AuditAction
from app.api.deps import get_current_user
from app.config import settings

router = APIRouter(tags=["Reports"])


@router.post(
    "/inspections/{inspection_id}/report",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate PDF compliance inspection report",
)
def create_report(
    inspection_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generates official ReportLab PDF with declarations, scores, findings, and remarks."""
    report = report_service.generate_pdf_report(db, inspection_id, user_id=current_user.id)
    client_ip = request.client.host if request.client else None
    audit_service.log_event(
        db=db,
        action=AuditAction.REPORT_GENERATED,
        user_id=current_user.id,
        entity_type="Report",
        entity_id=str(report.id),
        ip_address=client_ip,
        metadata={"report_number": report.report_number, "inspection_id": inspection_id},
    )
    return report


@router.get("/reports/{report_id}", response_model=ReportResponse, summary="Get report metadata")
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve metadata of a generated report."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "REPORT_NOT_FOUND", "message": "Report not found."},
        )
    return report


@router.get("/reports/{report_id}/download", summary="Download report PDF")
def download_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Download the actual PDF file."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "REPORT_NOT_FOUND", "message": "Report not found."},
        )
    
    filename = os.path.basename(report.storage_url)
    pdf_path = os.path.join(settings.REPORT_DIR, filename)

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "FILE_NOT_FOUND", "message": "PDF file is not available on disk."},
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{report.report_number}.pdf",
    )
