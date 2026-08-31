from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    product_name: str
    brand: str | None = None
    category: str | None = "Packaged Commodity"
    manufacturer: str | None = None
    packer: str | None = None
    importer: str | None = None
    batch_number: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: str | None = None
    brand: str | None = None
    category: str | None = None
    manufacturer: str | None = None
    packer: str | None = None
    importer: str | None = None
    batch_number: str | None = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

