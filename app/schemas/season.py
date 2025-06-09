from pydantic import BaseModel


class SeasonBase(BaseModel):
    description: str
    year: int


class SeasonCreate(SeasonBase):
    pass


class Season(SeasonBase):
    id: int

    class ConfigDict:
        from_attributes = True
