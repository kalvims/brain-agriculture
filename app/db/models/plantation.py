from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Plantation(Base):
    __tablename__ = "plantations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    farm_plantations = relationship(
        "FarmPlantationSeason",
        back_populates="plantation")
