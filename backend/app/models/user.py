from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base, TimestampMixin
from app.utils.constants import UserRole


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum"),
        default=UserRole.INSPECTOR,
        nullable=False,
    )
    department: Mapped[str] = mapped_column(String(100), nullable=True, default="Legal Metrology Department")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    inspections = relationship("Inspection", back_populates="inspector", cascade="all, delete-orphan")
    reviews = relationship("InspectorReview", back_populates="inspector", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="generator", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
