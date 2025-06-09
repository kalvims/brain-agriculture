from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.session import get_db
from app.schemas.plantation import Plantation, PlantationCreate
from app.services.plantation_service import PlantationService

router = APIRouter()
session = get_db()


@router.get("/", response_model=list[Plantation])
def list_plantations(
    *,
    session: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    plantation_service = PlantationService(db=session)
    return plantation_service.list_plantations(offset=offset, limit=limit)


@router.post("/", response_model=Plantation)
def create_plantation(
    *,
    plantation: PlantationCreate,
    session: Session = Depends(get_db),
):
    plantation_service = PlantationService(db=session)
    return plantation_service.create_plantation(plantation)


@router.get("/{plantation_id}", response_model=Plantation)
def get_plantation(*, plantation_id: int, session: Session = Depends(get_db)):
    plantation_service = PlantationService(db=session)
    return plantation_service.get_plantation_by_id(plantation_id)


@router.put("/{plantation_id}", response_model=Plantation)
def update_plantation(
    *,
    session: Session = Depends(get_db),
    plantation_id: int,
    plantation: PlantationCreate,
):
    plantation_service = PlantationService(db=session)
    return plantation_service.update_plantation(plantation_id, plantation)


@router.delete("/{plantation_id}", response_model=Plantation)
def delete_plantation(*, session: Session = Depends(get_db),
                      plantation_id: int):
    plantation_service = PlantationService(db=session)
    return plantation_service.remove_plantation(plantation_id)
