from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.utils.constants import DeclarationType, DeclarationStatus
from app.schemas.image import BoundingBox


class DeclarationBase(BaseModel):
    type: DeclarationType
    value: Optional[str] = None
    confidence: float = 0.0
    status: DeclarationStatus = DeclarationStatus.DETECTED
    image_id: Optional[int] = None
    bbox: Optional[BoundingBox] = None


class DeclarationCreate(DeclarationBase):
    inspection_id: int


class DeclarationResponse(DeclarationBase):
    id: int
    inspection_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

