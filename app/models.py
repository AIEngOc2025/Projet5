from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from .database import Base

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