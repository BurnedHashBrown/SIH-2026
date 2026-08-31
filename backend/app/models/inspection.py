from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base, TimestampMixin
from app.utils.constants import InspectionStatus


class Inspection(Base, TimestampMixin):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    inspection_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    inspector_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    location: Mapped[str] = mapped_column(String(150), nullable=True, default="Field Inspection")
    inspection_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    status: Mapped[InspectionStatus] = mapped_column(
        Enum(InspectionStatus, name="inspection_status_enum"),
        default=InspectionStatus.DRAFT,
        nullable=False,
    )
    compliance_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_checks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    passed_checks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    review_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    violation_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    product = relationship("Product", back_populates="inspections")
    inspector = relationship("User", back_populates="inspections")
    images = relationship("InspectionImage", back_populates="inspection", cascade="all, delete-orphan")
    declarations = relationship("Declaration", back_populates="inspection", cascade="all, delete-orphan")
    violations = relationship("Violation", back_populates="inspection", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="inspection", cascade="all, delete-orphan")
