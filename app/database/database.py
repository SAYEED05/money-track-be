import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase


load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env')


db_url = os.getenv('DB_URL')
if not db_url:
    raise RuntimeError('DB_URL environment variable is required')

db_echo = os.getenv('DB_ECHO', 'true').lower() in {'1', 'true', 'yes', 'on'}

engine = create_engine(db_url, echo=db_echo)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class Base(DeclarativeBase):
    pass