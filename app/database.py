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
#%% creation du modèle des données 
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func

#%% Définition des modèles SQLAlchemy

## enregistrement des entrées utilisateur 

class UserInputRecord(Base):
    __tablename__ = "user_inputs"

    id = Column(Integer, primary_key=True, index=True)
    # On stocke les entrées brutes
    property_gfa_total = Column(Float, nullable=False)
    year_built = Column(Integer, nullable=False)
    building_type = Column(String, nullable=False)
    # Optionnel : on peut stocker l'IP ou le User-Agent pour l'analyse
    user_metadata = Column(String, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

#%% enregistrement des prédictions
class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    property_gfa_total = Column(Float, nullable=False)
    year_built = Column(Integer, nullable=False)
    building_type = Column(String, nullable=False)
    prediction_value = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())