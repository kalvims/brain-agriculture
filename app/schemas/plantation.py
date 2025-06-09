from pydantic import BaseModel


class PlantationBase(BaseModel):
    name: str
    description: str


class PlantationCreate(PlantationBase):
    pass


class Plantation(PlantationBase):
    id: int

    class ConfigDict:
        from_attributes = True
