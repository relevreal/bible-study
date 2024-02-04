from app.models.base import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Unicode,
    UniqueConstraint,
)


class OriginalWord(Base):
    __tablename__ = "original_word"

    id = Column(Integer(), primary_key=True, index=True)
    word = Column(Unicode(64), nullable=False)
    transliteration = Column(Unicode(64), nullable=False)
    language_id = Column(Integer(), ForeignKey("language.id"), nullable=False)

    UniqueConstraint(word, transliteration, language_id)