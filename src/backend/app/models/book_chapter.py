from app.models.base import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)


class BookChapter(Base):
    __tablename__ = "book_chapter"

    id = Column(Integer(), primary_key=True, index=True)
    number = Column(Integer(), nullable=False)
    book_id = Column(Integer(), ForeignKey("book.id"), nullable=False)

    UniqueConstraint(number, book_id)
