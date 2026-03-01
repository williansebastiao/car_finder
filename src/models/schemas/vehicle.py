from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VehicleFilters(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    fuel: Optional[str] = None
    transmission: Optional[str] = None
    color: Optional[str] = None
    condition: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    max_mileage: Optional[int] = None


class VehicleResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    brand: str
    model: str
    year: int
    color: str
    fuel: str
    transmission: str
    engine: str
    doors: int
    mileage: int
    price: Decimal
    condition: str
    category: str
