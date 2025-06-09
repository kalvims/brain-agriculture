from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.session import get_db
from app.schemas.season import Season, SeasonCreate
from app.services.season_service import SeasonService

router = APIRouter()
session = get_db()


@router.get("/", response_model=list[Season])
def list_seasons(
    *,
    session: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    season_service = SeasonService(db=session)
    return season_service.list_seasons(offset=offset, limit=limit)


@router.post("/", response_model=Season)
def create_season(
    *,
    season: SeasonCreate,
    session: Session = Depends(get_db),
):
    season_service = SeasonService(db=session)
    return season_service.create_season(season)


@router.get("/{season_id}", response_model=Season)
def get_season(*, season_id: int, session: Session = Depends(get_db)):
    season_service = SeasonService(db=session)
    return season_service.get_season_by_id(season_id)


@router.put("/{season_id}", response_model=Season)
def update_season(
    *, session: Session = Depends(get_db), season_id: int, season: SeasonCreate
):
    season_service = SeasonService(db=session)
    return season_service.update_season(season_id, season)


@router.delete("/{season_id}", response_model=Season)
def delete_season(*, session: Session = Depends(get_db), season_id: int):
    season_service = SeasonService(db=session)
    return season_service.remove_season(season_id)
