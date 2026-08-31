from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.utils.constants import PanelType


class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float


class ImageQualityResult(BaseModel):
    quality_score: float
    is_acceptable: bool
    warnings: List[str] = []
    blur_score: Optional[float] = None
    brightness_score: Optional[float] = None
    contrast_score: Optional[float] = None


class ImageUploadResponse(BaseModel):
    image_id: int
    file_name: str
    panel_type: PanelType
    quality_score: float
    storage_url: str
    width: int
    height: int
    is_acceptable: bool
    warnings: List[str] = []


class ImageResponse(BaseModel):
    id: int
    inspection_id: int
    file_name: str
    storage_url: str
    panel_type: PanelType
    image_quality_score: float
    width: int
    height: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

