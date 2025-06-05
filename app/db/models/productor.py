from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db.session import Base

class Productor(Base):
    __tablename__ = "productors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cpf_cnpj = Column(String, unique=True, nullable=False)
    birthdate = Column(Date, nullable=False)

    farms = relationship("Farm", back_populates="productor") 