from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.farm_plantation_season import FarmPlantationSeason
from app.db.models.plantation import Plantation
from app.schemas.plantation import PlantationCreate


class PlantationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_plantation(self, plantation: PlantationCreate):
        db_plantation = Plantation(
            name=plantation.name, description=plantation.description
        )
        self.db.add(db_plantation)
        self.db.commit()
        self.db.refresh(db_plantation)
        return db_plantation

    def get_plantation_by_id(self, plantation_id: int):
        return self.db.query(Plantation).filter(
            Plantation.id == plantation_id).first()

    def list_plantations(self, offset: int = 0, limit: int = 100):
        return self.db.query(Plantation).offset(offset).limit(limit).all()

    def update_plantation(self, plantation_id: int,
                          plantation: PlantationCreate):
        db_plantation = self.get_plantation_by_id(plantation_id)
        if db_plantation:
            db_plantation.name = plantation.name
            db_plantation.description = plantation.description
            self.db.commit()
            self.db.refresh(db_plantation)
        return db_plantation

    def remove_plantation(self, plantation_id: int):
        plantation = self.get_plantation_by_id(plantation_id)
        if plantation:
            self.db.delete(plantation)
            self.db.commit()
        return plantation

    def get_plantations_statistics(self):
        results = (
            self.db.query(
                FarmPlantationSeason.season_id,
                FarmPlantationSeason.plantation_id,
                func.count(FarmPlantationSeason.plantation_id).label(
                    "total_plantations"
                ),
            )
            .group_by(
                FarmPlantationSeason.season_id, FarmPlantationSeason.plantation_id
            )
            .all()
        )
        return results

    def get_plantations_total_by_season(self):
        seasons_plantation_total = (
            self.db.query(
                FarmPlantationSeason.season_id,
                func.count(FarmPlantationSeason.plantation_id).label(
                    "total_plantations"
                ),
            )
            .group_by(FarmPlantationSeason.season_id)
            .all()
        )
        return seasons_plantation_total
