from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from app.utils.constants import PanelType


class InspectionImage(Base):
    __tablename__ = "inspection_images"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    inspection_id: Mapped[int] = mapped_column(ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_url: Mapped[str] = mapped_column(String(500), nullable=False)
    panel_type: Mapped[PanelType] = mapped_column(
        Enum(PanelType, name="panel_type_enum"),
        default=PanelType.FRONT,
        nullable=False,
    )
    image_quality_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    width: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    height: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    inspection = relationship("Inspection", back_populates="images")
    ocr_results = relationship("OCRResult", back_populates="image", cascade="all, delete-orphan")
    declarations = relationship("Declaration", back_populates="image", cascade="all, delete-orphan")
