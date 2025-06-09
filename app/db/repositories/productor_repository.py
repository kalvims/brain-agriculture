from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.models.productor import Productor
from app.schemas.productor import ProductorCreate


class ProductorRepository:
    def __init__(self, db: Session):
        self.db = db

    def productor_exists(self, productor_id: int) -> bool:
        productor = (
            self.db.query(Productor).filter(
                Productor.id == productor_id).first()
        )
        return productor is not None

    def create_productor(self, productor: ProductorCreate):
        db_productor = Productor(
            name=productor.name,
            cpf_cnpj=productor.cpf_cnpj,
            birthdate=productor.birthdate,
        )
        self.db.add(db_productor)
        self.db.commit()
        self.db.refresh(db_productor)
        return db_productor

    def get_productor_by_id(self, productor_id: int):
        return self.db.query(Productor).filter(
            Productor.id == productor_id).first()

    def list_productors(self, offset: int = 0, limit: int = 100):
        return self.db.query(Productor).offset(offset).limit(limit).all()

    def update_productor(self, productor_id: int, productor: ProductorCreate):
        db_productor = self.get_productor_by_id(productor_id)
        if db_productor:
            db_productor.name = productor.name
            db_productor.cpf_cnpj = productor.cpf_cnpj
            db_productor.birthdate = productor.birthdate
            self.db.commit()
            self.db.refresh(db_productor)
        return db_productor

    def remove_productor(self, productor_id: int):
        productor = self.get_productor_by_id(productor_id)
        if productor:
            self.db.delete(productor)
            self.db.commit()
        return productor

    def get_productor_by_cpf_cnpj(self, cpf_cnpj: str):
        return self.db.query(Productor).filter(
            Productor.cpf_cnpj == cpf_cnpj).first()
