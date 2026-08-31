from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base, TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    brand: Mapped[str] = mapped_column(String(100), index=True, nullable=True)
    category: Mapped[str] = mapped_column(String(100), index=True, nullable=True, default="Packaged Commodity")
    manufacturer: Mapped[str] = mapped_column(String(255), nullable=True)
    packer: Mapped[str] = mapped_column(String(255), nullable=True)
    importer: Mapped[str] = mapped_column(String(255), nullable=True)
    batch_number: Mapped[str] = mapped_column(String(100), index=True, nullable=True)

    # Relationships
    inspections = relationship("Inspection", back_populates="product", cascade="all, delete-orphan")
