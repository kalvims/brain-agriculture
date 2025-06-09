from datetime import date

from pydantic import BaseModel


class ProductorBase(BaseModel):
    name: str
    cpf_cnpj: str
    birthdate: date


class ProductorCreate(ProductorBase):
    pass


class Productor(ProductorBase):
    id: int

    class ConfigDict:
        from_attributes = True
