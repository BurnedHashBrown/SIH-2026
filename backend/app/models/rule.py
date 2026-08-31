from datetime import datetime
from sqlalchemy import String, Boolean, Text, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base, TimestampMixin
from app.utils.constants import DeclarationType, ValidationType, RuleSeverity


class Rule(Base, TimestampMixin):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    rule_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), default="General", nullable=False)
    declaration_type: Mapped[DeclarationType] = mapped_column(
        Enum(DeclarationType, name="declaration_type_rule_enum"),
        nullable=False,
    )
    validation_type: Mapped[ValidationType] = mapped_column(
        Enum(ValidationType, name="validation_type_enum"),
        default=ValidationType.PRESENCE,
        nullable=False,
    )
    severity: Mapped[RuleSeverity] = mapped_column(
        Enum(RuleSeverity, name="rule_severity_enum"),
        default=RuleSeverity.HIGH,
        nullable=False,
    )
    version: Mapped[str] = mapped_column(String(20), default="1.0", nullable=False)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_to: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    violations = relationship("Violation", back_populates="rule")
