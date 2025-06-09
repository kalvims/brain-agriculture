from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.session import get_db
from app.schemas.reports import (
    GroundUseStatistics,
    PlantationStatistics,
    StateStatistics,
    TotalArea,
    TotalFarms,
)
from app.services.reports_service import ReportsService

router = APIRouter()
session = get_db()


@router.get("/total-farms", response_model=TotalFarms)
def get_total_farms(
    *,
    session: Session = Depends(get_db),
):
    reports_service = ReportsService(db=session)
    return reports_service.get_total_farms()


@router.get("/total-area", response_model=TotalArea)
def get_total_area(
    *,
    session: Session = Depends(get_db),
):
    reports_service = ReportsService(db=session)
    return reports_service.get_total_area()


@router.get("/state-statistics", response_model=list[StateStatistics])
def get_state_statistics(
    *,
    session: Session = Depends(get_db),
):
    reports_service = ReportsService(db=session)
    return reports_service.get_state_statistics()


@router.get("/plantation-statistics",
            response_model=list[PlantationStatistics])
def get_plantation_statistics(
    *,
    session: Session = Depends(get_db),
):
    reports_service = ReportsService(db=session)
    return reports_service.get_plantation_statistics()


@router.get("/ground-use-statistics", response_model=GroundUseStatistics)
def get_ground_use_statistics(
    *,
    session: Session = Depends(get_db),
):
    reports_service = ReportsService(db=session)
    return reports_service.get_ground_use_statistics()
