"""ce script contient les schémas Pydantic pour la validation des données d'entrée et
de sortie de l'API."""
#%% app/schemas.py
from pydantic import BaseModel, ConfigDict,Field
from datetime import datetime
from typing import Optional

#%% Schéma de base pour les données d'entrée (ce que l'utilisateur envoie)
class PredictionBase(BaseModel):
    property_gfa_total: float
    year_built: int
    building_type: str

    # Ajout des champs supplémentaires pour la prédiction complète
    primary_property_type: Optional[str] = "Other"
    neighborhood: Optional[str] = "DOWNTOWN"
    council_district_code: Optional[int] = 1
    number_of_buildings: Optional[int] = 1
    number_of_floors: Optional[int] = 1
    property_gfa_parking: Optional[float] = 0
    energy_stars_energy_star_score: Optional[float] = 50
    steam_use_kBtu_: Optional[float] = 0
    natural_gas_therms_: Optional[float] = 0
    compliance_status: Optional[str] = "Compliant"
    ghg_emissions_intensity: Optional[float] = 0  
#%% Schéma utilisé pour la création de données (peut être étendu si besoin)
class PredictionCreate(BaseModel):
    property_gfa_total: float = Field(..., gt=0) # Doit être > 0
    year_built: int = Field(..., ge=1800, le=2026) # Année réaliste
    building_type: str

#%% Schéma de réponse (ce que l'API renvoie, incluant les données générées par la DB)
class PredictionResponse(PredictionBase):
    id: int
    prediction_value: float
    created_at: datetime

    # Permet à Pydantic de lire les données même si ce sont des objets SQLAlchemy
    model_config = ConfigDict(from_attributes=True)