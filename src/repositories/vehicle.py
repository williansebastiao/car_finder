from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.entities.vehicle import VehicleModel
from src.models.schemas.vehicle import VehicleFilters


class VehicleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def search(
        self, filters: VehicleFilters, limit: int = 10
    ) -> list[VehicleModel]:
        query = select(VehicleModel)
        conditions = []

        if filters.brand:
            conditions.append(VehicleModel.brand.ilike(f"%{filters.brand}%"))

        if filters.model:
            conditions.append(VehicleModel.model.ilike(f"%{filters.model}%"))

        if filters.year_min is not None:
            conditions.append(VehicleModel.year >= filters.year_min)

        if filters.year_max is not None:
            conditions.append(VehicleModel.year <= filters.year_max)

        if filters.fuel:
            conditions.append(VehicleModel.fuel.ilike(f"%{filters.fuel}%"))

        if filters.transmission:
            conditions.append(
                VehicleModel.transmission.ilike(f"%{filters.transmission}%")
            )

        if filters.color:
            conditions.append(VehicleModel.color.ilike(f"%{filters.color}%"))

        if filters.condition:
            conditions.append(
                VehicleModel.condition.ilike(f"%{filters.condition}%")
            )

        if filters.category:
            conditions.append(
                VehicleModel.category.ilike(f"%{filters.category}%")
            )

        if filters.min_price is not None:
            conditions.append(VehicleModel.price >= filters.min_price)

        if filters.max_price is not None:
            conditions.append(VehicleModel.price <= filters.max_price)

        if filters.max_mileage is not None:
            conditions.append(VehicleModel.mileage <= filters.max_mileage)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.limit(limit).order_by(VehicleModel.price.asc())

        result = await self._session.execute(query)
        return list(result.scalars().all())
