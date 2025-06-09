from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    farm_plantations = relationship(
        "FarmPlantationSeason",
        back_populates="season")
