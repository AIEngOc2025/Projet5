
#%% importations des librairies
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

#%% création de l'application FastAPI
app = FastAPI(title="Futurisys Building Energy API")

#%% Chargement du modèle
model = joblib.load("/Users/mpaga/Desktop/OC/Projets/Projet5/models/model_energy.joblib")

#%% Définition du schéma de données (Pydantic)
class BuildingData(BaseModel):
    Surface: float
    YearBuilt: int
    PropertyType: str

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de prédiction Futurisys"}

@app.post("/predict")
def predict(data: BuildingData):
    try:
        # Transformation en DataFrame pour le modèle
        df = pd.DataFrame([data.model_dump()])
        prediction = model.predict(df)
        return {"prediction": prediction[0], "unit": "kgCO22"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))