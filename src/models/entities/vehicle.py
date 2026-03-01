from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.entities.base import BaseModel


class VehicleModel(BaseModel):
    __tablename__ = "vehicles"

    brand: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    color: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    fuel: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    transmission: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    engine: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    doors: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    mileage: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )
    condition: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    def __repr__(self):
        return f"Vehicle(id={self.id}, brand={self.brand}, model={self.model}, year={self.year})"
