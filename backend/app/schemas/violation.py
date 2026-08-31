from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.utils.constants import ViolationType, ViolationStatus, RuleSeverity, ReviewDecision
from app.schemas.image import BoundingBox


class InspectorReviewCreate(BaseModel):
    decision: ReviewDecision
    remarks: Optional[str] = None


class InspectorReviewResponse(BaseModel):
    id: int
    violation_id: int
    inspector_id: int
    decision: ReviewDecision
    remarks: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ViolationResponse(BaseModel):
    id: int
    inspection_id: int
    rule_id: Optional[int] = None
    declaration_id: Optional[int] = None
    type: ViolationType
    description: str
    severity: RuleSeverity
    confidence: float
    status: ViolationStatus
    evidence_image_id: Optional[int] = None
    declaration_type: Optional[str] = None
    rule_code: Optional[str] = None
    reviews: List[InspectorReviewResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ViolationEvidenceResponse(BaseModel):
    violation_id: int
    image_id: Optional[int]
    image_url: Optional[str]
    panel_type: Optional[str]
    bbox: Optional[BoundingBox]
    description: str

