from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.utils.constants import InspectionStatus
from app.schemas.product import ProductResponse
from app.schemas.image import ImageResponse
from app.schemas.declaration import DeclarationResponse
from app.schemas.violation import ViolationResponse


class InspectionCreate(BaseModel):
    product_name: str
    brand: Optional[str] = None
    category: Optional[str] = "Packaged Commodity"
    manufacturer: Optional[str] = None
    packer: Optional[str] = None
    importer: Optional[str] = None
    batch_number: Optional[str] = None
    location: Optional[str] = "Field Inspection"


class InspectionUpdate(BaseModel):
    location: Optional[str] = None
    status: Optional[InspectionStatus] = None


class InspectionSummary(BaseModel):
    total_checks: int
    passed: int
    review: int
    violations: int


class InspectionResponse(BaseModel):
    id: int
    inspection_id: str
    product_id: int
    inspector_id: Optional[int] = None
    location: str
    inspection_date: datetime
    status: InspectionStatus
    compliance_score: float
    total_checks: int
    passed_checks: int
    review_count: int
    violation_count: int
    created_at: datetime
    updated_at: datetime
    product: Optional[ProductResponse] = None

    model_config = ConfigDict(from_attributes=True)


class InspectionDetailResponse(InspectionResponse):
    images: List[ImageResponse] = []
    declarations: List[DeclarationResponse] = []
    violations: List[ViolationResponse] = []


class AnalysisResponse(BaseModel):
    inspection_id: str
    compliance_score: float
    status: InspectionStatus
    summary: InspectionSummary
    declarations: List[DeclarationResponse]
    violations: List[ViolationResponse]

