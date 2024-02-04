from app.models.base import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    UniqueConstraint,
)


class Verse(Base):
    __tablename__ = "verse"

    id = Column(Integer(), primary_key=True, index=True)
    number = Column(Integer(), nullable=False)
    book_chapter_id = Column(Integer(), ForeignKey("book_chapter.id"), nullable=False)
    heading_id = Column(Integer(), ForeignKey("heading.id"), nullable=True)

    UniqueConstraint(number, book_chapter_id, heading_id)
