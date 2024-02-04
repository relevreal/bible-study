import csv
from enum import IntEnum
import os
import glob

from sqlalchemy import (
    create_engine,
    select,
)
from sqlalchemy.dialects.sqlite import insert

from app import models

SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///./app/bible.db"
BIBLE_DIR = "./data/berean"
OLD_TESTAMENT = "old_testament"
NEW_TESTAMENT = "new_testament"


class Col(IntEnum):
    HEB_SORT = 0
    GRK_SORT = 1
    BSB_SORT = 2
    LANGUAGE = 3
    VS = 4
    ORIGINAL_WORD = 5
    TRANSLIT = 6
    PARSING = 7
    PARSING_DETAILED = 8
    STRONGS = 9
    VERSE = 10
    HEADING = 11
    CROSS_REFERENCES = 12
    BSB_VERSION = 13
    FOOTNOTES = 14
    BDB_THAYERS = 15


def main():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
    with engine.connect() as conn:
        insert_language_stmt = (
            insert(models.Language)
            .values([
                {"language": "Hebrew"},
                {"language": "Greek"},
            ])
            .on_conflict_do_nothing(index_elements=["language"])
        )
        conn.execute(insert_language_stmt)
        select_hebrew_stmt = select(models.Language.id).where(models.Language.language == "Hebrew")
        select_greek_stmt = select(models.Language.id).where(models.Language.language == "Greek")
        hebrew_id = conn.execute(select_hebrew_stmt).first()[0]
        greek_id = conn.execute(select_greek_stmt).first()[0]
        print(f"Added Hebrew with id {hebrew_id} and Greek with id: {greek_id}")
        add_bible(conn, hebrew_id, greek_id)


def add_bible(conn, hebrew_id, greek_id):
    for testament, language_id in zip((OLD_TESTAMENT, NEW_TESTAMENT), (hebrew_id, greek_id)):
        for book_path in sorted(glob.glob(os.path.join(BIBLE_DIR, testament, "*.csv")), key=_extract_book_sequence):
            book_sequence = _extract_book_sequence(book_path)
            add_bible_book(conn, book_path, language_id, hebrew_id, book_sequence)


def _extract_book_sequence(book_path):
    return int(book_path.split("/")[-1].split("_")[0])


def add_bible_book(conn, book_path, language_id, hebrew_id, book_sequence):
    curr_chapter = None
    curr_chapter_id = None
    curr_heading_id = None
    book_title = book_path.split('/')[-1].split("_")[1].split('.')[0]

    insert_book_stmt = (
        insert(models.Book)
        .values(
            title=book_title,
            sequence=book_sequence,
        )
    )
    result = conn.execute(insert_book_stmt)
    book_id = result.inserted_primary_key[0]
    print(f"Adding book: {book_title} [id: {book_id}]")

    with open(book_path) as f:
        csv_reader = csv.reader(f, delimiter=",")
        # skip header
        next(csv_reader)
        for i, row in enumerate(csv_reader):
            if row[Col.HEADING]:
                insert_heading_stmt = (
                    insert(models.Heading)
                    .values(title=row[Col.HEADING])
                    .on_conflict_do_nothing(index_elements=["title"])
                )
                result = conn.execute(insert_heading_stmt)
                curr_heading_id = result.inserted_primary_key[0]
            if row[Col.VERSE]:
                verse = row[Col.VERSE]
                chapter_verse = verse.split(" ")[-1].split(":")
                next_chapter = int(chapter_verse[0])
                curr_verse = int(chapter_verse[1])
                if next_chapter != curr_chapter:
                    insert_chapter_stmt = (
                        insert(models.BookChapter)
                        .values(
                            number=next_chapter,
                            book_id=book_id,
                        )
                    )
                    result = conn.execute(insert_chapter_stmt)
                    conn.commit()
                    curr_chapter_id = result.inserted_primary_key[0]
                    curr_chapter = next_chapter

                insert_verse_stmt = (
                    insert(models.Verse)
                    .values(
                        number=curr_verse,
                        book_chapter_id=curr_chapter_id,
                        heading_id=curr_heading_id,
                    )
                )
                result = conn.execute(insert_verse_stmt)
                curr_verse_id = result.inserted_primary_key[0]
                curr_heading_id = None

            insert_original_word_stmt = (
                insert(models.OriginalWord)
                .values(
                    word=row[Col.ORIGINAL_WORD],
                    transliteration=row[Col.TRANSLIT],
                    language_id=language_id,
                )
                .on_conflict_do_nothing(index_elements=["word", "transliteration", "language_id"])
            )
            result = conn.execute(insert_original_word_stmt)
            original_word_id = result.inserted_primary_key[0]

            insert_bible_word_stmt = (
                insert(models.BibleWord)
                .values(
                    location=row[Col.HEB_SORT] if language_id == hebrew_id else row[Col.GRK_SORT],
                    bsb_location=row[Col.BSB_SORT],
                    bsb_version=row[Col.BSB_VERSION],
                    original_word_id=original_word_id,
                    verse_id=curr_verse_id,
                    strongs_number_id=row[Col.STRONGS]
                )
            )
            conn.execute(insert_bible_word_stmt)
        conn.commit()


if __name__ == "__main__":
    main()
