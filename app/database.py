"""Module de configuration de la base de données et définition des modèles de données 
pour l'application FastAPI utilisant SQLAlchemy et PostgreSQL."""
# ==========================================================================================
#%% configuration de la base de données avec SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base # declarative_base a bougé dans .orm dans les versions récentes
import os

# Configuration de l'URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:projet5@localhost:5432/futurisys_db")

# L'engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de données déclarative
Base = declarative_base()

# Dépendance FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================================================================
