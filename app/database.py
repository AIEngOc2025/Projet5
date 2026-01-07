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

#%% creation du modèle des données 
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    property_gfa_total = Column(Float, nullable=False)
    year_built = Column(Integer, nullable=False)
    building_type = Column(String, nullable=False)
    prediction_value = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())