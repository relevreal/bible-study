from app.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
)


class Heading(Base):
    __tablename__ = "heading"

    id = Column(Integer(), primary_key=True, index=True)
    title = Column(String(64), nullable=False, unique=True)

