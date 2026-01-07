from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import engine, get_db

# Création des tables dans la base de données (si elles n'existent pas)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Futurisys ML API",
    description="API de prédiction de consommation énergétique pour les bâtiments.",
    version="1.0.0"
)

# Fonction simulée du modèle ML (À remplacer par l'import de ton vrai modèle .pkl)
def mock_ml_predict(data: schemas.PredictionCreate) -> float:
    # Ici, on simule une logique de calcul simple
    # En production : return model.predict(X)
    return (data.property_gfa_total * 0.15) + (2025 - data.year_built) * 0.5

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Futurisys. Accédez à /docs pour la documentation."}

@app.post("/predict", response_model=schemas.PredictionResponse)
def predict_energy(payload: schemas.PredictionCreate, db: Session = Depends(get_db)):
    """
    Réalise une prédiction et enregistre le résultat en base de données.
    """
    try:
        # 1. Calcul de la prédiction via le moteur ML
        prediction_value = mock_ml_predict(payload)
        
        # 2. Persistance dans PostgreSQL via le CRUD
        new_record = crud.create_prediction(
            db=db, 
            prediction_data=payload, 
            pred_value=prediction_value
        )
        
        return new_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")

@app.get("/history", response_model=List[schemas.PredictionResponse])
def get_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère l'historique des dernières prédictions.
    """
    return crud.get_predictions(db, skip=skip, limit=limit)