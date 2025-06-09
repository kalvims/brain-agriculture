from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.session import Base


class FarmPlantationSeason(Base):
    __tablename__ = "farm_plantation_season"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    plantation_id = Column(
        Integer,
        ForeignKey("plantations.id"),
        nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)

    # Relacionamentos com Farm, Plantation e Season
    farm = relationship("Farm", back_populates="farm_plantations")
    plantation = relationship("Plantation", back_populates="farm_plantations")
    season = relationship("Season", back_populates="farm_plantations")
