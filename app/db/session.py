from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from app.db.models.productor import Productor
from app.db.models.farm import Farm
from app.db.models.plantation import Plantation
from app.db.models.season import Season

Base.metadata.create_all(bind=engine) 