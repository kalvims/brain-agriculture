from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.session import Base

farm_plantation = Table(
    "farm_plantation",
    Base.metadata,
    Column("farm_id", Integer, ForeignKey("farms.id"), primary_key=True),
    Column("plantation_id", Integer, ForeignKey("plantations.id"), primary_key=True),
) 