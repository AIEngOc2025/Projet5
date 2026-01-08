"""
Fichier principal finalisé pour le POC Futurisys.
Gère l'inférence avec le modèle réel (46 colonnes) et la persistance PostgreSQL.
"""
import joblib
import pandas as pd
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, get_db

# Stockage global du modèle pour éviter de le recharger à chaque requête
ml_models = {}

@asynccontextmanager
async def lifespan(api: FastAPI):
    """ Gestion du chargement du modèle au démarrage de l'API """
    model_path = Path(__file__).parent.parent / "models" / "model_energy.joblib"
    if not model_path.exists():
        raise FileNotFoundError(f"Modèle introuvable à : {model_path}")
    
    # Chargement du Pipeline complet
    ml_models["energy_model"] = joblib.load(model_path)
    print("✅ Pipeline ML chargé et prêt pour l'inférence.")
    yield
    ml_models.clear()

# Création des tables PostgreSQL
models.Base.metadata.create_all(bind=engine)

api = FastAPI(
    title="Futurisys ML API", 
    version="1.0.0", 
    lifespan=lifespan,
    description="API industrielle pour la prédiction énergétique."
)

@api.get("/")
def read_root():
    return {"message": "API Futurisys opérationnelle. Accédez à /docs pour tester."}

@api.post("/predict", response_model=schemas.PredictionResponse)
def predict_energy(payload: schemas.PredictionCreate, db: Session = Depends(get_db)):
    """
    Endpoint principal : reçoit 3 paramètres, complète les 46 colonnes, 
    prédit et enregistre en base de données.
    """
    try:
        # 1. Préparation du dictionnaire complet exigé par le ColumnTransformer
        # On injecte les données de l'UI et on complète avec des valeurs neutres
        full_data = {
            # Données issues de l'utilisateur
            "PropertyGFATotal": payload.property_gfa_total,
            "YearBuilt": payload.year_built,
            "BuildingType": payload.building_type,
            
            # Colonnes obligatoires pour le modèle (valeurs par défaut/moyennes)
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

        # Conversion en DataFrame (format requis par Scikit-Learn)
        input_df = pd.DataFrame([full_data])

        # 2. Inférence via le Pipeline chargé en mémoire
        model = ml_models["energy_model"]
        prediction_result = model.predict(input_df)
        
        # Extraction de la valeur (souvent un tableau numpy de taille 1)
        prediction_value = float(prediction_result[0])

        # 3. Sauvegarde dans la base de données PostgreSQL (Traçabilité)
        new_record = crud.create_prediction(
            db=db, 
            prediction_data=payload, 
            pred_value=prediction_value
        )
        
        return new_record

    except ValueError as ve:
        # Capture les erreurs de colonnes ou de types
        raise HTTPException(status_code=422, detail=f"Erreur de formatage des données : {str(ve)}")
    except Exception as e:
        # Capture toute autre erreur (DB, Pipeline, etc.)
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {str(e)}")

@api.get("/history", response_model=List[schemas.PredictionResponse])
def get_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """ Récupère l'historique des prédictions enregistrées """
    return crud.get_predictions(db, skip=skip, limit=limit)