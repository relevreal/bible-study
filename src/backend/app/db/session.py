from app.core.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI.unicode_string(), connect_args={"check_same_thread": False},
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
