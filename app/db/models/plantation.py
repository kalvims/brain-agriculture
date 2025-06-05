from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.farm_plantation import farm_plantation

class Plantation(Base):
    __tablename__ = "plantations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    season_id = Column(Integer, ForeignKey("seasons.id"))
    season = relationship("Season", back_populates="plantations")

    farms = relationship(
        "Farm",
        secondary=farm_plantation,
        back_populates="plantations"
    ) 