import csv
import os
import sys

import pandas as pd
from openpyxl import load_workbook


BSB_TABLES = "../../data/bsb_tables.xlsx"
HEBREW_WORD_COL = "WLC / Nestle Base {TR} ⧼RP⧽ (WH) 〈NE〉 [NA] ‹SBL› [[ECM]]"
COL_TO_SKIP = " ⇔ "


def main():
    wb = None
    try:
        wb = load_workbook(BSB_TABLES, read_only=True)
        ws = wb.active
        data = ws.values
        # skip first row
        next(data)
        cols = next(data)
        cols = list(col for col in cols if col is not None)
        HEBREW_WORD_COL_IDX = next((i for i, col in enumerate(cols) if col == HEBREW_WORD_COL), None)
        if HEBREW_WORD_COL_IDX is None:
            print(f"Couldn't find '{HEBREW_WORD_COL}' column in: {cols}")
            sys.exit(1)
        cols[HEBREW_WORD_COL_IDX] = "Original Word" 
        COL_TO_SKIP_IDX = next((i for i, col in enumerate(cols) if col == COL_TO_SKIP), None)
        n_cols = len(cols)
        print(cols)
        data = list(data)
        print(f"Data length: {len(data)}")
        if COL_TO_SKIP_IDX is not None:
            cleaned_data_generator = (
                row[:COL_TO_SKIP_IDX] + row[COL_TO_SKIP_IDX+1:n_cols]
                for row in data
                if row[0] is not None # and row[3] == "Hebrew"
            ) 
            cols = cols[:COL_TO_SKIP_IDX] + cols[COL_TO_SKIP_IDX+1:]
        else:
            cleaned_data_generator = (
                row[:n_cols]
                for row in data
                if row[0] is not None and row[3] == "Hebrew"
            ) 
        insert_data(cleaned_data_generator, cols)
    finally:
        if wb is not None: wb.close()


def insert_data(data_generator, cols):
    VERSE_COL_IDX = next((i for i, col in enumerate(cols) if col == "Verse"), None)
    LANGUAGE_COL_IDX = next((i for i, col in enumerate(cols) if col == "Language"), None)
    if VERSE_COL_IDX is None:
        print(f"Couldn't find 'Verse' column in: {cols}")
        sys.exit(1)
    if LANGUAGE_COL_IDX is None:
        print(f"Couldn't find 'Language' column in: {cols}")
        sys.exit(1)
    FILENAME_TEMPLATE = "../backend/data/{bible_dir}/{old_or_new_testament}/{number}_{bible_book}.csv"
    old_or_new_testament = "old_testament"
    curr_book = None
    curr_book_number = 1
    curr_book_chapter = None
    curr_verse = None
    curr_file = None
    csv_writer = None
    try:
        for i, row in enumerate(data_generator):
            if row[LANGUAGE_COL_IDX] == "Greek":
                old_or_new_testament = "new_testament"
            if row[VERSE_COL_IDX] is not None:
                verse = row[VERSE_COL_IDX]
                verse_splitted = verse.split(" ")
                next_book = " ".join(verse_splitted[:-1])
                chapter_verse = verse_splitted[-1].split(":")
                next_book_chapter = int(chapter_verse[0])
                curr_verse = int(chapter_verse[1])
                if curr_book_chapter != next_book_chapter:
                    curr_book_chapter = next_book_chapter
                if curr_book is None or curr_book != next_book:
                    curr_book = next_book
                    if curr_file is not None:
                        curr_file.close()
                        curr_file = None
                    filename = FILENAME_TEMPLATE.format(
                        bible_dir="berean",
                        old_or_new_testament=old_or_new_testament,
                        number=curr_book_number,
                        bible_book=curr_book.lower(),
                    )
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    curr_file = open(filename, "w", newline="")
                    csv_writer = csv.writer(curr_file, delimiter=",")
                    csv_writer.writerow(cols)
                    print(f"{old_or_new_testament}/{curr_book_number}_{curr_book}")
                    curr_book_number += 1
            if csv_writer is None:
                print(f"Csv writer is set to 'None' when trying to write row {i}: {row}")
                sys.exit(1)
            csv_writer.writerow(row)
    finally:
        if curr_file != None and not curr_file.closed:
            curr_file.close()



if __name__ == "__main__":
    main()