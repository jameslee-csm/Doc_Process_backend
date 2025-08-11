from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from langchain_community.utilities import SQLDatabase
import os

# Database URL - using SQLite for simplicity
DATABASE_URL = "sqlite:///./legal_documents.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_langchain_db() -> SQLDatabase:
    """Get SQLDatabase instance for langchain
    
    Returns:
        SQLDatabase: A langchain SQLDatabase instance configured with the current engine
    """
    return SQLDatabase(engine=engine)
