from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DB_USER = os.getenv("AUDIT_DB_USER", "postgres")
DB_PASSWORD = os.getenv("AUDIT_DB_PASSWORD", "postgres")
DB_HOST = os.getenv("AUDIT_DB_HOST", "localhost")
DB_PORT = os.getenv("AUDIT_DB_PORT", "5432")
DB_NAME = os.getenv("AUDIT_DB_NAME", "audit_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
