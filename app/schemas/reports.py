from pydantic import BaseModel

from app.schemas.plantation import Plantation


class TotalFarms(BaseModel):
    total_farms: int


class TotalArea(BaseModel):
    total_area: float


class PlantationSeasonStatistics(BaseModel):
    plantation_id: int
    total_plantations: int
    percent: float


class PlantationStatistics(BaseModel):
    season_id: int
    season_plantations_total: int
    statistics: list[PlantationSeasonStatistics]


class PlantationStateStatistics(BaseModel):
    percent: float
    state_total: int


class GroundUseStatistics(BaseModel):
    vegetation_area_percent: float
    vegetation_area_total: float
    arable_area_percent: float
    arable_area_total: float
    total_area: float


class StateStatistics(BaseModel):
    state: str
    farms_total: int
    farms_percent: float
    plantation_statistics: PlantationStateStatistics
    ground_use_statistics: GroundUseStatistics
