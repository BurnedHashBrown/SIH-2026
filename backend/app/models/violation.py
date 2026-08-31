from sqlalchemy import String, Float, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base, TimestampMixin
from app.utils.constants import ViolationType, ViolationStatus, RuleSeverity


class Violation(Base, TimestampMixin):
    __tablename__ = "violations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    inspection_id: Mapped[int] = mapped_column(ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)
    rule_id: Mapped[int] = mapped_column(ForeignKey("rules.id", ondelete="SET NULL"), nullable=True)
    declaration_id: Mapped[int] = mapped_column(ForeignKey("declarations.id", ondelete="SET NULL"), nullable=True)
    type: Mapped[ViolationType] = mapped_column(
        Enum(ViolationType, name="violation_type_enum"),
        default=ViolationType.REVIEW_REQUIRED,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[RuleSeverity] = mapped_column(
        Enum(RuleSeverity, name="violation_severity_enum"),
        default=RuleSeverity.HIGH,
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[ViolationStatus] = mapped_column(
        Enum(ViolationStatus, name="violation_status_enum"),
        default=ViolationStatus.AI_DETECTED,
        nullable=False,
    )
    evidence_image_id: Mapped[int] = mapped_column(ForeignKey("inspection_images.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    inspection = relationship("Inspection", back_populates="violations")
    rule = relationship("Rule", back_populates="violations")
    declaration = relationship("Declaration", back_populates="violations")
    evidence_image = relationship("InspectionImage")
    reviews = relationship("InspectorReview", back_populates="violation", cascade="all, delete-orphan")
