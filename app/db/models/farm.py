from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    total_area = Column(Float, nullable=False)
    arable_area = Column(Float, nullable=False)
    vegetation_area = Column(Float, nullable=False)

    productor_id = Column(Integer, ForeignKey("productors.id"))
    productor = relationship("Productor", back_populates="farms")

    # Relacionamento com a tabela associativa
    farm_plantations = relationship(
        "FarmPlantationSeason",
        back_populates="farm")
