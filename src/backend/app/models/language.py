from app.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
)


class Language(Base):
    __tablename__ = "language"

    id = Column(Integer(), primary_key=True, index=True)
    language = Column(String(64), nullable=False, unique=True)