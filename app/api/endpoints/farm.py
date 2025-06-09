from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.session import get_db
from app.schemas.farm import Farm, FarmCreate, FarmPlantation, FarmSeason
from app.schemas.farm_plantation_season import (
    FarmPlantationSeason,
    FarmPlantationSeasonCreate,
)
from app.services.farm_service import FarmService

router = APIRouter()
session = get_db()


@router.get("/", response_model=list[Farm])
def list_farms(
    *,
    session: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    farm_service = FarmService(db=session)
    return farm_service.list_farms(offset=offset, limit=limit)


@router.post("/", response_model=Farm)
def create_farm(
    *,
    farm: FarmCreate,
    session: Session = Depends(get_db),
):
    farm_service = FarmService(db=session)
    return farm_service.create_farm(farm)


@router.get("/{farm_id}", response_model=Farm)
def get_farm(*, farm_id: int, session: Session = Depends(get_db)):
    farm_service = FarmService(db=session)
    return farm_service.get_farm_by_id(farm_id)


@router.put("/{farm_id}", response_model=Farm)
def update_farm(*, session: Session = Depends(get_db),
                farm_id: int, farm: FarmCreate):
    farm_service = FarmService(db=session)
    return farm_service.update_farm(farm_id, farm)


@router.put("/{farm_id}/add-plantation", response_model=FarmPlantationSeason)
def add_plantation(
    *,
    session: Session = Depends(get_db),
    farm_id: int,
    plantation_season: FarmPlantationSeasonCreate,
):
    farm_service = FarmService(db=session)
    return farm_service.add_plantation(farm_id, plantation_season)


@router.delete("/{farm_id}", response_model=Farm)
def delete_farm(*, session: Session = Depends(get_db), farm_id: int):
    farm_service = FarmService(db=session)
    return farm_service.remove_farm(farm_id)


@router.get("/{farm_id}/plantations", response_model=list[FarmPlantation])
def get_farm_plantations(*, farm_id: int, session: Session = Depends(get_db)):
    farm_service = FarmService(db=session)
    return farm_service.get_farm_plantations(farm_id)


@router.get("/{farm_id}/seasons", response_model=list[FarmSeason])
def get_farm_seasons(*, farm_id: int, session: Session = Depends(get_db)):
    farm_service = FarmService(db=session)
    return farm_service.get_farm_seasons(farm_id)
