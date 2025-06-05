from sqlalchemy.orm import Session
from app.db.models.productor import Productor

class ProductorRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar_productor(self, name: str, cpf_cnpj: str, birthdate: str):
        productor = Productor(name=name, cpf_cnpj=cpf_cnpj, birthdate=birthdate)
        self.db.add(productor)
        self.db.commit()
        self.db.refresh(productor)
        return productor

    def obter_productor_by_id(self, productor_id: int):
        return self.db.query(Productor).filter(Productor.id == productor_id).first()

    def list_productors(self):
        return self.db.query(Productor).all()

    def update_productor(self, productor_id: int, name: str, cpf_cnpj: str, birthdate: str):
        productor = self.obter_productor_by_id(productor_id)
        if productor:
            productor.name = name
            productor.cpf_cnpj = cpf_cnpj
            productor.birthdate = birthdate
            self.db.commit()
            self.db.refresh(productor)
        return productor

    def deletar_productor(self, productor_id: int):
        productor = self.obter_productor_by_id(productor_id)
        if productor:
            self.db.delete(productor)
            self.db.commit()
        return productor 