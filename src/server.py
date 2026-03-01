import json
from typing import Optional

from mcp.server.fastmcp import FastMCP

from src.database.session import AsyncSessionFactory
from src.models.schemas.vehicle import VehicleFilters, VehicleResult
from src.repositories.vehicle import VehicleRepository

mcp = FastMCP("car-finder")


@mcp.tool()
async def search_vehicles(
    brand: Optional[str] = None,
    model: Optional[str] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    fuel: Optional[str] = None,
    transmission: Optional[str] = None,
    color: Optional[str] = None,
    condition: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    max_mileage: Optional[int] = None,
) -> str:
    filters = VehicleFilters(
        brand=brand,
        model=model,
        year_min=year_min,
        year_max=year_max,
        fuel=fuel,
        transmission=transmission,
        color=color,
        condition=condition,
        category=category,
        min_price=min_price,
        max_price=max_price,
        max_mileage=max_mileage,
    )

    async with AsyncSessionFactory() as session:
        repo = VehicleRepository(session)
        vehicles = await repo.search(filters)

    results = [
        VehicleResult.model_validate(v).model_dump(mode="json")
        for v in vehicles
    ]

    return json.dumps(results, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
