""" Ce script créé des modèles de données pour les entrées utilisateurs
et les prédictions"""
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base


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


#%% crerr la classe prediction 
class PredictionRecord(Base):
    __tablename__ = "predictions"
    # Cette ligne permet de recharger le modèle sans erreur
    #__table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    property_gfa_total = Column(Float, nullable=False)
    year_built = Column(Integer, nullable=False)
    building_type = Column(String, nullable=False)
    prediction_value = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())