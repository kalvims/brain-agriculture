from sqlalchemy.orm import Session

from app.db.models.season import Season
from app.schemas.season import SeasonCreate


class SeasonRepository:
    def __init__(self, db: Session):
        self.db = db

    def season_exists(self, season_id: int) -> bool:
        season = self.db.query(Season).filter(Season.id == season_id).first()
        return season is not None

    def create_season(self, season: SeasonCreate):
        db_season = Season(
            description=season.description,
            year=season.year,
        )
        self.db.add(db_season)
        self.db.commit()
        self.db.refresh(db_season)
        return db_season

    def get_season_by_id(self, season_id: int):
        return self.db.query(Season).filter(Season.id == season_id).first()

    def list_seasons(self, offset: int = 0, limit: int = 100):
        return self.db.query(Season).offset(offset).limit(limit).all()

    def update_season(self, season_id: int, season: SeasonCreate):
        db_season = self.get_season_by_id(season_id)
        if db_season:
            db_season.description = season.description
            db_season.year = season.year
            self.db.commit()
            self.db.refresh(db_season)
        return db_season

    def remove_season(self, season_id: int):
        season = self.get_season_by_id(season_id)
        if season:
            self.db.delete(season)
            self.db.commit()
        return season
