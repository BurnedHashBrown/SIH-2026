from datetime import datetime, timezone
from sqlalchemy import Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from app.utils.constants import ReviewDecision


class InspectorReview(Base):
    __tablename__ = "inspector_reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    violation_id: Mapped[int] = mapped_column(ForeignKey("violations.id", ondelete="CASCADE"), nullable=False)
    inspector_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    decision: Mapped[ReviewDecision] = mapped_column(
        Enum(ReviewDecision, name="review_decision_enum"),
        nullable=False,
    )
    remarks: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    violation = relationship("Violation", back_populates="reviews")
    inspector = relationship("User", back_populates="reviews")
