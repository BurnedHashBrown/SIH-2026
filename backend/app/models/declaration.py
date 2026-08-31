from sqlalchemy import String, Float, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base, TimestampMixin
from app.utils.constants import DeclarationType, DeclarationStatus


class Declaration(Base, TimestampMixin):
    __tablename__ = "declarations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    inspection_id: Mapped[int] = mapped_column(ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)
    image_id: Mapped[int] = mapped_column(ForeignKey("inspection_images.id", ondelete="SET NULL"), nullable=True)
    type: Mapped[DeclarationType] = mapped_column(
        Enum(DeclarationType, name="declaration_type_enum"),
        nullable=False,
    )
    value: Mapped[str] = mapped_column(Text, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[DeclarationStatus] = mapped_column(
        Enum(DeclarationStatus, name="declaration_status_enum"),
        default=DeclarationStatus.DETECTED,
        nullable=False,
    )
    bbox_x: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)
    bbox_y: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)
    bbox_width: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)
    bbox_height: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)

    # Relationships
    inspection = relationship("Inspection", back_populates="declarations")
    image = relationship("InspectionImage", back_populates="declarations")
    violations = relationship("Violation", back_populates="declaration")
