from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ReportResponse(BaseModel):
    id: int
    inspection_id: int
    report_number: str
    storage_url: str
    generated_by: Optional[int] = None
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)

