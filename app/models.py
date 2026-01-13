from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from .database import Base

#%% créé une entrée donnée utilisateur
class UserInputRecord(Base):
    __tablename__ = "user_inputs"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    property_gfa_total = Column(Float)
    year_built = Column(Integer)
    building_type = Column(String)
    # Ajoute les autres colonnes si tu veux tout stocker, 
    # ou assure-toi que ton crud ne sauvegarde que ce qui existe
#%% 
class PredictionRecord(Base):
    __tablename__ = "predictions"
    # Cette ligne permet de recharger le modèle sans erreur
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    property_gfa_total = Column(Float, nullable=False)
    year_built = Column(Integer, nullable=False)
    building_type = Column(String, nullable=False)
    prediction_value = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())