"""create database schema

Revision ID: ae9b6f537fc4
Revises: 
Create Date: 2023-11-24 16:57:54.497847

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ae9b6f537fc4"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table("book",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_book")),
        sa.UniqueConstraint("title", name=op.f("uq_book_title")),
        sa.UniqueConstraint("sequence", name=op.f("uq_book_sequence")),
    )
    op.create_index(op.f("ix_book_id"), "book", ["id"], unique=False)

    op.create_table("heading",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_heading")),
        sa.UniqueConstraint("title", name=op.f("uq_heading_title")),
    )
    op.create_index(op.f("ix_heading_id"), "heading", ["id"], unique=False)

    op.create_table("language",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("language", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_language")),
        sa.UniqueConstraint("language", name=op.f("uq_language_language")),
    )
    op.create_index(op.f("ix_language_id"), "language", ["id"], unique=False)

    op.create_table("strongs_number",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_strongs_number")),
    )
    op.create_index(op.f("ix_strongs_number_id"), "strongs_number", ["id"], unique=False)

    op.create_table("book_chapter",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["book.id"], name=op.f("fk_book_chapter_book_id_book")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_book_chapter")),
        sa.UniqueConstraint("number", "book_id", name=op.f("uq_book_chapter_number_book_id_")),
    )
    op.create_index(op.f("ix_book_chapter_id"), "book_chapter", ["id"], unique=False)

    op.create_table("original_word",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("word", sa.Unicode(length=64), nullable=False),
        sa.Column("transliteration", sa.Unicode(length=64), nullable=False),
        sa.Column("language_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["language_id"], ["language.id"], name=op.f("fk_original_word_language_id_language")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_original_word")),
        sa.UniqueConstraint("word", "transliteration", "language_id", name=op.f("uq_original_word_word_transliteration_language_id")),
    )
    op.create_index(op.f("ix_original_word_id"), "original_word", ["id"], unique=False)

    op.create_table("verse",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("book_chapter_id", sa.Integer(), nullable=False),
        sa.Column("heading_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["book_chapter_id"], ["book_chapter.id"], name=op.f("fk_verse_book_chapter_id_book_chapter")),
        sa.ForeignKeyConstraint(["heading_id"], ["heading.id"], name=op.f("fk_verse_heading_id_heading")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_verse")),
        sa.UniqueConstraint("number", "book_chapter_id", "heading_id", name=op.f("uq_verse_number_book_chapter_id_heading_id")),
    )
    op.create_index(op.f("ix_verse_id"), "verse", ["id"], unique=False)

    op.create_table("bible_word",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("location", sa.Integer(), nullable=False),
        sa.Column("bsb_location", sa.Integer(), nullable=False),
        sa.Column("bsb_version", sa.String(64), nullable=False),
        sa.Column("original_word_id", sa.Unicode(length=64), nullable=False),
        sa.Column("verse_id", sa.Integer(), nullable=False),
        sa.Column("strongs_number_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["strongs_number_id"], ["strongs_number.id"], name=op.f("fk_bible_word_strongs_number_id_strongs_number")),
        sa.ForeignKeyConstraint(["verse_id"], ["verse.id"], name=op.f("fk_bible_word_verse_id_verse")),
        sa.ForeignKeyConstraint(["original_word_id"], ["original_word.id"], name=op.f("fk_bible_word_original_word_id_original_word")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_bible_word")),
    )
    op.create_index(op.f("ix_bible_word_id"), "bible_word", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_bible_word_id"), table_name="bible_word")
    op.drop_table("bible_word")

    op.drop_index(op.f("ix_verse_id"), table_name="verse")
    op.drop_table("verse")

    op.drop_index(op.f("ix_original_word_id"), table_name="original_word")
    op.drop_table("original_word")

    op.drop_index(op.f("ix_book_chapter_id"), table_name="book_chapter")
    op.drop_table("book_chapter")

    op.drop_index(op.f("ix_strongs_number_id"), table_name="strongs_number")
    op.drop_table("strongs_number")

    op.drop_index(op.f("ix_language_id"), table_name="language")
    op.drop_table("language")

    op.drop_index(op.f("ix_heading_id"), table_name="heading")
    op.drop_table("heading")

    op.drop_index(op.f("ix_book_id"), table_name="book")
    op.drop_table("book")
