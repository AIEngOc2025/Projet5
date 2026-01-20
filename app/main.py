"""
Fichier principal finalisé pour le POC Futurisys.
Intégration MLflow pour la gestion du cycle de vie et persistance PostgreSQL.
"""
# ==========================================================================================
#%% IMPORTATIONS DES BIBLIOTHEQUES
import joblib
import pandas as pd
import mlflow.sklearn  # Ajout de MLflow
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from . models import get_db
from . database import engine

#=========================================================================================
#%% Stockage global du modèle et des métadonnées
ml_models = {}

@asynccontextmanager
async def lifespan(api: FastAPI):
    """ Gestion du chargement du modèle via MLflow au démarrage """
    
    # Nom du modèle défini dans ton script d'entraînement MLflow
    model_name = "model_energy_minmax"
    model_uri = f"models:/{model_name}/latest"
    
    try:
        # Tentative de chargement via le Model Registry de MLflow
        print(f"Tentative de chargement du modèle depuis MLflow : {model_uri}...")
        ml_models["energy_model"] = mlflow.sklearn.load_model(model_uri)
        ml_models["model_version"] = "MLflow latest"
        print("Pipeline ML chargé depuis MLflow.")
        
    except Exception as e:
        print(f"Échec MLflow ({e}). Repli sur le fichier local joblib...")
        # Fallback sur le fichier local si MLflow n'est pas disponible
        model_path = Path(__file__).parent.parent / "models" / "model_energy.joblib"
        if not model_path.exists():
            raise FileNotFoundError(f"Aucun modèle trouvé (MLflow ou Local) à : {model_path}")
        
        ml_models["energy_model"] = joblib.load(model_path)
        ml_models["model_version"] = "Local Joblib File"
        print("Pipeline ML chargé depuis le fichier local.")

    yield
    ml_models.clear()

#%% Création des tables PostgreSQL (décommenter si nécessaire)
# models.Base.metadata.create_all(bind=engine)

#%% Initialisation de l'API FastAPI
api = FastAPI(
    title="Futurisys ML API", 
    version="1.1.0", # Montée de version pour l'intégration MLflow
    lifespan=lifespan,
    description="API industrielle avec gestion de cycle de vie MLflow."
)

@api.get("/")
def read_root():
    return {
        "status": "online",
        "model_source": ml_models.get("model_version", "Non chargé"),
        "docs": "/docs"
    }

@api.post("/predict", response_model=schemas.PredictionResponse)
def predict_energy(payload: schemas.PredictionCreate, db: Session = Depends(get_db)):
    """
    Endpoint principal : Inférence via le modèle MLflow (MinMaxScaler intégré).
    """
    try:
        # 1. Préparation des données (14 colonnes requises par le preprocessor)
        full_data = {
            "PropertyGFATotal": payload.property_gfa_total,
            "YearBuilt": payload.year_built,
            "BuildingType": payload.building_type,
            "PrimaryPropertyType": "Other",
            "Neighborhood": "DOWNTOWN",
            "CouncilDistrictCode": 1,
            "NumberofBuildings": 1,
            "NumberofFloors": 1,
            "PropertyGFAParking": 0,
            "ENERGYSTARScore": 50,
            "SteamUse(kBtu)": 0,
            "NaturalGas(therms)": 0,
            "ComplianceStatus": "Compliant",
            "GHGEmissionsIntensity": 0
        }

        # 2. Sauvegarde de l'entrée utilisateur
        crud.save_user_input(db, full_data)

        # 3. Inférence
        input_df = pd.DataFrame([full_data])
        model = ml_models["energy_model"]
        prediction_result = model.predict(input_df)
        
        # Le modèle prédit un log, on repasse en valeur réelle (exp - 1) 
        # si ton script d'entraînement utilise np.log1p
        prediction_value = float(np.expm1(prediction_result[0]))

        # 4. Sauvegarde de la prédiction
        new_record = crud.create_prediction(
            db=db, 
            prediction_data=payload, 
            pred_value=prediction_value
        )
        
        return new_record

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'inférence : {str(e)}")

@api.get("/history", response_model=List[schemas.PredictionResponse])
def get_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_predictions(db, skip=skip, limit=limit)