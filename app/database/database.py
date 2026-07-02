import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env', override=True)


db_url = os.getenv('DB_URL')
if not db_url:
    raise RuntimeError('DB_URL environment variable is required')

db_echo = os.getenv('DB_ECHO', 'true').lower() in {'1', 'true', 'yes', 'on'}

# Normalize DB_URL to the asyncpg driver so an existing psycopg2 URL still works.
if '+asyncpg' not in db_url:
    db_url = db_url.replace('+psycopg2', '+asyncpg').replace('postgresql://', 'postgresql+asyncpg://', 1)

engine = create_async_engine(db_url, echo=db_echo)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as session:
        yield session
