from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.farm import Farm
from app.schemas.productor import Productor, ProductorCreate
from app.services.productor_service import ProductorService

router = APIRouter()


@router.get("/", response_model=list[Productor])
def list_productors(
    *,
    session: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    # tables = session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    # print("Tabelas disponíveis na  LIST:", tables)
    productor_service = ProductorService(session)
    return productor_service.list_productors(offset=offset, limit=limit)


@router.post("/", response_model=Productor)
def create_productor(
    *,
    productor: ProductorCreate,
    session: Session = Depends(get_db),
):
    # tables = session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    # print("Tabelas disponíveis na sessão CREATE:", tables)
    productor_service = ProductorService(session)
    return productor_service.create_productor(productor)


@router.get("/{productor_id}", response_model=Productor)
def get_productor(*, productor_id: int, session: Session = Depends(get_db)):
    productor_service = ProductorService(session)
    return productor_service.get_productor_by_id(productor_id)


@router.put("/{productor_id}", response_model=Productor)
def update_productor(
    *, session: Session = Depends(get_db), productor_id: int, productor: ProductorCreate
):
    productor_service = ProductorService(session)
    return productor_service.update_productor(productor_id, productor)


@router.delete("/{productor_id}", response_model=Productor)
def delete_productor(*, session: Session = Depends(get_db), productor_id: int):
    productor_service = ProductorService(session)
    return productor_service.delete_productor(productor_id)


@router.get("/{productor_id}/farms", response_model=list[Farm])
def get_productor_farms(*, productor_id: int,
                        session: Session = Depends(get_db)):
    productor_service = ProductorService(session)
    return productor_service.get_productor_farms(productor_id)
