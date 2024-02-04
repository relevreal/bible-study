from app.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
)


class StrongsNumber(Base):
    __tablename__ = "strongs_number"

    id = Column(Integer(), primary_key=True, index=True)
    number = Column(Integer(), nullable=False)