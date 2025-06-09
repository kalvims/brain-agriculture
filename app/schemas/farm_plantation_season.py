from pydantic import BaseModel

from app.schemas.plantation import Plantation
from app.schemas.season import Season


class FarmPlantationSeasonBase(BaseModel):
    plantation_id: int
    season_id: int


class FarmPlantationSeasonCreate(FarmPlantationSeasonBase):
    pass


class FarmPlantationSeason(FarmPlantationSeasonBase):
    id: int
    farm_id: int

    class ConfigDict:
        from_attributes = True


class PlantationSeason(Plantation):
    seasons: list[Season]


class SeasonPlantation(Season):
    plantations: list[Plantation]
