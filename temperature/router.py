from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.TemperatureRead])
async def read_all_temperatures(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_temperatures(db=db)


@router.get("/temperatures/{city_id}",
            response_model=list[schemas.TemperatureRead])
async def read_one_city_temperatures(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: int | None = None):
    temperatures = await crud.get_temperatures_for_one_city(
        db=db, city_id=city_id
    )
    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return temperatures


@router.post("/temperatures/update/",
             response_model=list[schemas.TemperatureRead])
async def update_temperatures(db: Annotated[AsyncSession, Depends(get_db)]):
    temperatures = await crud.get_update_on_temp_in_all_cities(db=db)
    return temperatures
