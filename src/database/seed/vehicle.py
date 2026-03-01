import asyncio
import random
from dataclasses import dataclass
from decimal import Decimal

from src.database.session import AsyncSessionFactory
from src.models.entities.vehicle import VehicleModel
from src.models.enums import (
    Brand,
    CarModel,
    Category,
    Color,
    Condition,
    Doors,
    Engine,
    Fuel,
    Transmission,
)


@dataclass(frozen=True)
class CarSpec:
    brand: Brand
    model: CarModel
    category: Category
    engines: tuple[Engine, ...]


CATALOG: list[CarSpec] = [
    CarSpec(
        Brand.TOYOTA, CarModel.COROLLA, Category.SEDAN, (Engine.MOTOR_2_0,)
    ),
    CarSpec(
        Brand.TOYOTA, CarModel.HILUX, Category.PICKUP, (Engine.MOTOR_3_0,)
    ),
    CarSpec(Brand.TOYOTA, CarModel.YARIS, Category.HATCH, (Engine.MOTOR_1_5,)),
    CarSpec(Brand.TOYOTA, CarModel.SW4, Category.SUV, (Engine.MOTOR_3_0,)),
    CarSpec(Brand.TOYOTA, CarModel.RAV4, Category.SUV, (Engine.MOTOR_2_5,)),
    CarSpec(Brand.HONDA, CarModel.CIVIC, Category.SEDAN, (Engine.MOTOR_2_0,)),
    CarSpec(Brand.HONDA, CarModel.HR_V, Category.SUV, (Engine.MOTOR_1_5,)),
    CarSpec(Brand.HONDA, CarModel.FIT, Category.HATCH, (Engine.MOTOR_1_5,)),
    CarSpec(Brand.HONDA, CarModel.CR_V, Category.SUV, (Engine.MOTOR_1_5,)),
    CarSpec(
        Brand.CHEVROLET, CarModel.ONIX, Category.HATCH, (Engine.MOTOR_1_0,)
    ),
    CarSpec(
        Brand.CHEVROLET, CarModel.TRACKER, Category.SUV, (Engine.MOTOR_1_0,)
    ),
    CarSpec(
        Brand.CHEVROLET, CarModel.SPIN, Category.MINIVAN, (Engine.MOTOR_1_0,)
    ),
    CarSpec(
        Brand.CHEVROLET, CarModel.CRUZE, Category.SEDAN, (Engine.MOTOR_1_4,)
    ),
    CarSpec(
        Brand.VOLKSWAGEN,
        CarModel.GOL,
        Category.HATCH,
        (Engine.MOTOR_1_0, Engine.MOTOR_1_6),
    ),
    CarSpec(
        Brand.VOLKSWAGEN, CarModel.POLO, Category.HATCH, (Engine.MOTOR_1_0,)
    ),
    CarSpec(
        Brand.VOLKSWAGEN, CarModel.VIRTUS, Category.SEDAN, (Engine.MOTOR_1_0,)
    ),
    CarSpec(
        Brand.VOLKSWAGEN, CarModel.TIGUAN, Category.SUV, (Engine.MOTOR_1_4,)
    ),
    CarSpec(
        Brand.VOLKSWAGEN, CarModel.AMAROK, Category.PICKUP, (Engine.MOTOR_2_0,)
    ),
    CarSpec(
        Brand.VOLKSWAGEN, CarModel.T_CROSS, Category.SUV, (Engine.MOTOR_1_0,)
    ),
    CarSpec(Brand.FORD, CarModel.KA, Category.HATCH, (Engine.MOTOR_1_0,)),
    CarSpec(Brand.FORD, CarModel.RANGER, Category.PICKUP, (Engine.MOTOR_2_0,)),
    CarSpec(Brand.FORD, CarModel.TERRITORY, Category.SUV, (Engine.MOTOR_1_5,)),
    CarSpec(Brand.FORD, CarModel.BRONCO, Category.SUV, (Engine.MOTOR_2_0,)),
    CarSpec(
        Brand.FIAT,
        CarModel.ARGO,
        Category.HATCH,
        (Engine.MOTOR_1_0, Engine.MOTOR_1_3),
    ),
    CarSpec(
        Brand.FIAT,
        CarModel.CRONOS,
        Category.SEDAN,
        (Engine.MOTOR_1_0, Engine.MOTOR_1_3),
    ),
    CarSpec(Brand.FIAT, CarModel.PULSE, Category.SUV, (Engine.MOTOR_1_0,)),
    CarSpec(
        Brand.FIAT,
        CarModel.TORO,
        Category.PICKUP,
        (Engine.MOTOR_1_3, Engine.MOTOR_2_0),
    ),
    CarSpec(Brand.FIAT, CarModel.STRADA, Category.PICKUP, (Engine.MOTOR_1_3,)),
    CarSpec(Brand.FIAT, CarModel.MOBI, Category.HATCH, (Engine.MOTOR_1_0,)),
    CarSpec(Brand.HYUNDAI, CarModel.HB20, Category.HATCH, (Engine.MOTOR_1_0,)),
    CarSpec(Brand.HYUNDAI, CarModel.CRETA, Category.SUV, (Engine.MOTOR_1_0,)),
    CarSpec(Brand.HYUNDAI, CarModel.TUCSON, Category.SUV, (Engine.MOTOR_1_6,)),
    CarSpec(
        Brand.HYUNDAI, CarModel.SANTA_FE, Category.SUV, (Engine.MOTOR_2_5,)
    ),
    CarSpec(Brand.RENAULT, CarModel.KWID, Category.HATCH, (Engine.MOTOR_1_0,)),
    CarSpec(
        Brand.RENAULT,
        CarModel.SANDERO,
        Category.HATCH,
        (Engine.MOTOR_1_0, Engine.MOTOR_1_6),
    ),
    CarSpec(Brand.RENAULT, CarModel.DUSTER, Category.SUV, (Engine.MOTOR_1_6,)),
    CarSpec(
        Brand.RENAULT,
        CarModel.LOGAN,
        Category.SEDAN,
        (Engine.MOTOR_1_0, Engine.MOTOR_1_6),
    ),
    CarSpec(Brand.JEEP, CarModel.RENEGADE, Category.SUV, (Engine.MOTOR_1_3,)),
    CarSpec(
        Brand.JEEP,
        CarModel.COMPASS,
        Category.SUV,
        (Engine.MOTOR_1_3, Engine.MOTOR_2_0),
    ),
    CarSpec(Brand.JEEP, CarModel.COMMANDER, Category.SUV, (Engine.MOTOR_1_3,)),
    CarSpec(Brand.JEEP, CarModel.WRANGLER, Category.SUV, (Engine.MOTOR_2_0,)),
]


def _build_vehicle() -> VehicleModel:
    spec = random.choice(CATALOG)
    condition = random.choice(list(Condition))

    return VehicleModel(
        brand=spec.brand,
        model=spec.model,
        category=spec.category,
        engine=random.choice(spec.engines),
        year=random.randint(2015, 2025),
        color=random.choice(list(Color)),
        fuel=random.choice(list(Fuel)),
        transmission=random.choice(list(Transmission)),
        doors=random.choice(list(Doors)),
        mileage=random.randint(0, 200_000),
        price=Decimal(random.randint(20_000, 350_000)),
        condition=condition,
    )


async def run_seed(total: int = 150) -> None:
    async with AsyncSessionFactory() as session:
        session.add_all(_build_vehicle() for _ in range(total))
        await session.commit()

    print(f"Seed concluído: {total} veículos inseridos.")


if __name__ == "__main__":
    asyncio.run(run_seed())
