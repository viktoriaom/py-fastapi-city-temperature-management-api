import datetime
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from city import crud as city_crud
from temperature import helpers, models


async def get_all_temperatures(db: AsyncSession) -> Any:
    result = await db.execute(
        select(models.Temperature)
    )
    temperatures = result.scalars().all()
    return temperatures


async def get_temperatures_for_one_city(db: AsyncSession, city_id) -> Any:
    result = await db.execute(
        select(models.Temperature).where(models.Temperature.city_id == city_id)
    )
    temperatures = result.scalars().all()
    return temperatures


async def get_update_on_temp_in_all_cities(db: AsyncSession) -> Any:
    cities = await city_crud.get_all_cities(db=db)
    for city in cities:
        temp = await helpers.get_city_temperature(city)
        if temp:
            db_temperature = models.Temperature(
                city_id=city.id,
                temperature=temp,
                date_time=datetime.datetime.now(),
            )
            db.add(db_temperature)
            await db.commit()
            await db.refresh(db_temperature)
        else:
            raise HTTPException(
                status_code=404, detail="Temperature not found"
            )

    temperatures = await get_all_temperatures(db)
    return temperatures
