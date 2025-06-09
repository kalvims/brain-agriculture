from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from app.db.models.farm import Farm
from app.db.models.farm_plantation_season import FarmPlantationSeason
from app.db.repositories.productor_repository import ProductorRepository
from app.schemas.farm import FarmCreate
from app.schemas.farm_plantation_season import FarmPlantationSeasonCreate


class FarmRepository:
    def __init__(self, db: Session):
        self.db = db
        self.productor_repo = ProductorRepository(db)

    def create_farm(self, farm: FarmCreate):
        db_farm = Farm(
            name=farm.name,
            city=farm.city,
            state=farm.state,
            total_area=farm.total_area,
            arable_area=farm.arable_area,
            vegetation_area=farm.vegetation_area,
            productor_id=farm.productor_id,
        )
        self.db.add(db_farm)
        self.db.commit()
        self.db.refresh(db_farm)
        return db_farm

    def add_plantation(
        self, farm_id: int, plantation_season: FarmPlantationSeasonCreate
    ):
        new_farm_plantation_season = FarmPlantationSeason(
            farm_id=farm_id,
            plantation_id=plantation_season.plantation_id,
            season_id=plantation_season.season_id,
        )
        self.db.add(new_farm_plantation_season)
        self.db.commit()
        self.db.refresh(new_farm_plantation_season)
        return new_farm_plantation_season

    def farm_plantation_exists(
        self, farm_id: int, plantation_season: FarmPlantationSeasonCreate
    ):
        db_farm_plantation = (
            self.db.query(FarmPlantationSeason)
            .filter(
                FarmPlantationSeason.farm_id == farm_id,
                FarmPlantationSeason.plantation_id == plantation_season.plantation_id,
                FarmPlantationSeason.season_id == plantation_season.season_id,
            )
            .first()
        )
        return db_farm_plantation is not None

    def get_farm_by_id(self, farm_id: int):
        return self.db.query(Farm).filter(Farm.id == farm_id).first()

    def list_farms(self, offset: int = 0, limit: int = 100):
        return self.db.query(Farm).offset(offset).limit(limit).all()

    def update_farm(self, farm_id: int, farm: FarmCreate):
        db_farm = self.get_farm_by_id(farm_id)
        if db_farm:
            db_farm.name = farm.name
            db_farm.city = farm.city
            db_farm.state = farm.state
            db_farm.total_area = farm.total_area
            db_farm.arable_area = farm.arable_area
            db_farm.vegetation_area = farm.vegetation_area
            db_farm.productor_id = farm.productor_id
            self.db.commit()
            self.db.refresh(db_farm)
        return db_farm

    def remove_farm(self, farm_id: int):
        farm = self.get_farm_by_id(farm_id)
        if farm:
            self.db.delete(farm)
            self.db.commit()
        return farm

    def get_total_farms(self):
        return self.db.query(Farm).count()

    def get_total_farms_by_state(self):
        return self.db.query(Farm.state, func.count()).group_by(Farm.state)

    def get_total_area(self):
        total_area = self.db.query(func.sum(Farm.total_area)).scalar()
        return total_area or 0

    def get_total_vegetation_area(self):
        total_vegetation_area = self.db.query(
            func.sum(Farm.vegetation_area)).scalar()
        return total_vegetation_area or 0

    def get_total_arable_area(self):
        total_arable_area = self.db.query(func.sum(Farm.arable_area)).scalar()
        return total_arable_area or 0

    def get_total_area_by_state(self):
        results = self.db.query(Farm.state, func.sum(Farm.total_area)).group_by(
            Farm.state
        )
        return results

    def get_vegetation_area_by_state(self):
        results = self.db.query(Farm.state, func.sum(Farm.vegetation_area)).group_by(
            Farm.state
        )
        return results

    def get_arable_area_by_state(self):
        results = self.db.query(Farm.state, func.sum(Farm.arable_area)).group_by(
            Farm.state
        )
        return results

    def get_total_plantations(self):
        total = self.db.query(
            distinct(
                FarmPlantationSeason.plantation_id)).count()
        return total

    def get_plantations_by_state(self):
        results = (
            self.db.query(
                Farm.state,
                func.count(distinct(FarmPlantationSeason.plantation_id)).label(
                    "state_plantations_total"
                ),
            )
            .join(FarmPlantationSeason, Farm.farm_plantations, isouter=True)
            .group_by(Farm.state)
            .all()
        )
        return results
