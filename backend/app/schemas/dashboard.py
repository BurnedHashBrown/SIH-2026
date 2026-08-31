from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict
from app.utils.constants import InspectionStatus


class DashboardSummaryResponse(BaseModel):
    total_inspections: int
    compliant: int
    potential_violations: int
    requires_review: int


class DashboardViolationsResponse(BaseModel):
    consumer_care: int
    mrp: int
    net_quantity: int
    manufacturer: int
    readability: int
    date_information: int
    other: int = 0


class RecentInspectionItem(BaseModel):
    id: int
    inspection_id: str
    product_name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    status: InspectionStatus
    compliance_score: float
    inspection_date: datetime

    model_config = ConfigDict(from_attributes=True)

