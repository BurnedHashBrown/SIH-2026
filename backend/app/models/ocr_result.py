from datetime import datetime, timezone
from sqlalchemy import Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base


class OCRResult(Base):
    __tablename__ = "ocr_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    image_id: Mapped[int] = mapped_column(ForeignKey("inspection_images.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    bbox_x: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    bbox_y: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    bbox_width: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    bbox_height: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    image = relationship("InspectionImage", back_populates="ocr_results")
