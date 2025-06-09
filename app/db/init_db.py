from app.db.models.farm import Farm
from app.db.models.farm_plantation_season import FarmPlantationSeason
from app.db.models.plantation import Plantation
from app.db.models.productor import Productor
from app.db.models.season import Season
from app.db.session import Base, engine


def init_db():
    Base.metadata.create_all(bind=engine)
