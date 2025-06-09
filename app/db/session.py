from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()


def get_db():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
