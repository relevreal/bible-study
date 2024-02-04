from app.models.base import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Unicode,
    String,
)


class BibleWord(Base):
    __tablename__ = "bible_word"

    id = Column(Integer(), primary_key=True, index=True)
    location = Column(Integer(), nullable=False)
    bsb_location = Column(Integer(), nullable=False)
    bsb_version = Column(String(64), nullable=False)
    original_word_id = Column(Unicode(64), ForeignKey("original_word.id"), nullable=False)
    verse_id = Column(Integer(), ForeignKey("verse.id"), nullable=False)
    strongs_number_id = Column(Integer(), ForeignKey("strongs_number.id"), nullable=False)
