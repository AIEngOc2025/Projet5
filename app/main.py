#%% importatations de bibliothèques
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models

#%% 1. Définition du schéma de données avec Pydantic
from pydantic import BaseModel, Field, field_validator # Import mis à jour
from typing import List

#%% CREATION AUTOMATIQUE DES TABLES DE DONNEES
from .database import engine
from . import models

# Cette ligne déclenche la création des tables dans PostgreSQL
models.Base.metadata.create_all(bind=engine)

class BuildingInput(BaseModel):
    PropertyGFATotal: float = Field(..., gt=0)
    YearBuilt: int = Field(..., gt=1800, lt=2026)
    BuildingType: str
    #NumFloors: int = Field(..., gt=0)
    #Features: List[str] = Field(default_factory=list)   

    @field_validator('BuildingType')
    @classmethod # Recommandé en Pydantic V2
    def validate_type(cls, v: str) -> str:
        allowed = ['Hotel', 'Office', 'Retail', 'Warehouse']
        if v not in allowed:
            # L'erreur sera proprement formatée en JSON par FastAPI
            raise ValueError(f"Type non supporté. Choix possibles : {allowed}")
        return v

#%% 2. Initialisation de l'API
app = FastAPI(
    title="Futurisys ML API",
    description="API de prédiction de consommation d'énergie et émissions CO2",
    version="1.0.0"
)

#%% 3. Chargement du modèle (Pipeline Scikit-Learn

try:
    model=joblib.load("models/model_energy.joblib")
    print("Modèle chargé avec succès.")
except Exception as e:
    print(f"Erreur de chargement du modèle : {e}")
    model = None

#%% 4. Endpoints
@app.get("/")
def health_check():
    return {"status": "online", "model_loaded": model is not None}


@app.post("/predict", response_model=dict)
def predict(data: BuildingInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    try:
        # Conversion Pydantic -> DataFrame (respecte l'ordre des features)
        input_df = pd.DataFrame([data.model_dump])
        
        # Calcul de la prédiction
        prediction = model.predict(input_df)
        
        return {
            "prediction": round(float(prediction[0]), 2),
            "unit": "kgCO2e",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")
    #%% 5. Intégration avec la base de données pour le logging (optionnel)
@app.post("/predict")
def predict(data: BuildingInput, db: Session = Depends(database.get_db)):
    # 1. Vérification du modèle
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    # 2. Calcul de la prédiction
    input_df = pd.DataFrame([data.dict()])
    prediction = model.predict(input_df)[0]
    
    # 3. SAUVEGARDE EN BASE DE DONNÉES
    db_prediction = models.PredictionRecord(
        property_gfa_total=data.PropertyGFATotal,
        year_built=data.YearBuilt,
        building_type=data.BuildingType,
        prediction_value=float(prediction)
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return {
        "id": db_prediction.id, # On renvoie l'ID de l'enregistrement
        "prediction": round(float(prediction), 2),
        "unit": "kgCO2e"
    }