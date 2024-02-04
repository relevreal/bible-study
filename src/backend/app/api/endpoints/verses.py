from itertools import groupby
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import (
    Session,
)
from sqlalchemy import (
    select,
    exc,
)
from pydantic import BaseModel
from loguru import logger as LOG

from app.api import deps
from app.models.verse import Verse
from app.models.book import Book
from app.models.book_chapter import BookChapter
from app.models.bible_word import BibleWord

router = APIRouter()

SessionDep = Annotated[Session, Depends(deps.get_db)]


class VerseSpan(BaseModel):
    start: int
    end: int


VersesOut = dict[str, dict[int, dict[int, list[str]]]]


@router.get("/{book_title}/{chapter}/{verses}")
@LOG.catch(reraise=True)
def get_verses(
    db: SessionDep,
    book_title: str,
    chapter: int,
    verses: int | str,
) -> VersesOut:
    try:
        book_id_stmt = select(Book.id).where(Book.title == book_title)
        book_id = db.execute(book_id_stmt).first()[0]
    except exc.SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while reading book: \"{book_title}\" from database",
        )
    if book_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with title: \"{book_title} not found",
        )
    try:
        book_chapter_id_stmt = (
            select(BookChapter.id)
            .where(BookChapter.book_id == book_id)
            .where(BookChapter.number == chapter)
        )
        book_chapter_id = db.execute(book_chapter_id_stmt).first()[0]
    except exc.SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while reading book: \"{verses.book}\" from database",
        )
    if book_chapter_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"\"{verses.title} {verses.chapter}\" chapter not found",
        )
    verses_db_stmt = select(Verse.id, Verse.number).where(Verse.book_chapter_id == book_chapter_id)
    verses_not_found_message = None
    if isinstance(verses, str) and ":" not in verses:
        verses = int(verses)
    if isinstance(verses, int):
        verses_db_stmt = verses_db_stmt.where(Verse.number == verses)
        verses_not_found_message = f"{book_title} {chapter} {verses} verse not found"
    elif isinstance(verses, str):
        verse_span = verses.split(":")
        start = int(verse_span[0])
        end = int(verse_span[1])
        verses_db_stmt = verses_db_stmt.where(
            Verse.number.between(
                start,
                end,
            )
        )
        verses_not_found_message = f"{book_title} {chapter} {start}:{end} verses not found"
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Something wrong with verses field, shouldn't be a str at this point",
        )
    verses_db = db.execute(verses_db_stmt).all()
    LOG.debug(
        "Retrieved the following verse ids: {verses_db}",
        verses_db=verses_db,
    )
    if verses_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=verses_not_found_message,
        )
    verse_ids = [v[0] for v in verses_db]
    verse_numbers = [v[1] for v in verses_db]
    verses_dict = {
        k: v
        for k, v in zip(verse_ids, verse_numbers)
    }
    bible_words_stmt = (
        select(BibleWord.verse_id, BibleWord.bsb_version)
        .where(BibleWord.verse_id.in_(verse_ids))
        .order_by(BibleWord.verse_id.asc(), BibleWord.bsb_location.asc())
    )
    bible_words = db.execute(bible_words_stmt).all()
    LOG.debug(
        "Retrieved the following bible words: {bible_words}",
        bible_words=bible_words
    )
    if bible_words is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Words associated with {book_title} {chapter} {verses} not found",
        )
    verses_grouped = {}
    for v_num, bws_gen in groupby(bible_words, lambda x: verses_dict[x[0]]):
        verses_grouped[v_num] = [bw[1].strip() for bw in bws_gen]
    LOG.debug(
        "Retrieved the following bible words: {verses_grouped}",
        verses_grouped=verses_grouped,
    )

    return {
        book_title: {
            chapter: verses_grouped,
        },
    }
