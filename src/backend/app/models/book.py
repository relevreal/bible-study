from app.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
)


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer(), primary_key=True, index=True)
    title = Column(String(64), nullable=False, unique=True)
    sequence = Column(Integer(), nullable=False, unique=True)
