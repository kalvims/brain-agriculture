from pydantic import BaseModel

from app.schemas.farm_plantation_season import PlantationSeason, SeasonPlantation


class FarmPlantation(PlantationSeason):
    pass


class FarmSeason(SeasonPlantation):
    pass


class FarmBase(BaseModel):
    name: str
    city: str
    state: str
    total_area: float
    arable_area: float
    vegetation_area: float
    productor_id: int


class FarmCreate(FarmBase):
    pass


class Farm(FarmBase):
    id: int

    class ConfigDict:
        from_attributes = True
