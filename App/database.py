from sqlalchemy import create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
import psycopg
from .models import Base
from sqlalchemy.orm import Session,sessionmaker

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',extra="ignore")
    DB_USERNAME:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:int
    DB_NAME:str
settings = Settings()

with psycopg.connect(
    dbname="postgres",
    user = settings.DB_USERNAME,
    password = settings.DB_PASSWORD,
    host = settings.DB_HOST,
    port = settings.DB_PORT
) as conn:
    conn.autocommit = True

    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'expense_tracker'")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("CREATE DATABASE expense_tracker")






engine = create_engine(f"postgresql+psycopg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
def get_session():
    with Session(engine) as session:
        yield session