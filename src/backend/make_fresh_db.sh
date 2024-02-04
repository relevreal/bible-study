#!/bin/bash

# Delete db if exists
db_filepath="./bible.db"
if [ -f $db_filepath ]; then
    rm $db_filepath
    echo "Removed $db_filepath"
fi

# Run alembic migrations to create up to date db
alembic upgrade head
echo "Ran alembic migrations"

# Populate db with data
python ./populate_db.py
echo "Populated db with data"

