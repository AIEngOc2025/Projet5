"""Schemas for the prediction API."""
#%% app/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

#%% Schéma de base pour les données d'entrée (ce que l'utilisateur envoie)
class PredictionBase(BaseModel):
    property_gfa_total: float
    year_built: int
    building_type: str

#%% Schéma utilisé pour la création (peut être étendu si besoin)
class PredictionCreate(PredictionBase):
    pass

#%% Schéma de réponse (ce que l'API renvoie, incluant les données générées par la DB)
class PredictionResponse(PredictionBase):
    id: int
    prediction_value: float
    created_at: datetime

    # Permet à Pydantic de lire les données même si ce sont des objets SQLAlchemy
    model_config = ConfigDict(from_attributes=True)