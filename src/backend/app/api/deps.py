from typing import Generator

from app.db.session import Session


def get_db() -> Generator:
    with Session() as session:
        yield session
