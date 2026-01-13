"""effectue des opérations crud sur les caractéristiques et les prédictions  dans la base de données."""

# =========================================================================================
#%% fonction CRUD pour enregistrer les entrées utilisateurs 

from sqlalchemy.orm import Session
from . import models, schemas

from .database import UserInputRecord

from .models import UserInputRecord

def save_user_input(db: Session, data: dict):
    db_input = UserInputRecord(
        property_gfa_total=data.get("PropertyGFATotal"),
        year_built=data.get("YearBuilt"),
        building_type=data.get("BuildingType")
    )
    db.add(db_input)
    db.commit() # Important pour persister avant la suite
    db.refresh(db_input)
    return db_input

#%% fonction CRUD pour les prédictions
def create_prediction(db: Session, prediction_data: schemas.PredictionCreate, pred_value: float):
    """
    Enregistre une nouvelle prédiction dans la base de données.
    """
    # 1. On crée une instance du modèle SQLAlchemy
    db_prediction = models.PredictionRecord(
        property_gfa_total=prediction_data.property_gfa_total,
        year_built=prediction_data.year_built,
        building_type=prediction_data.building_type,
        prediction_value=pred_value  # La valeur calculée par ton modèle ML
    )
    
    # 2. On l'ajoute et on valide la transaction
    db.add(db_prediction)
    db.commit()
    
    # 3. On rafraîchit l'objet pour récupérer l'ID et la date créés par Postgres
    db.refresh(db_prediction)
    
    return db_prediction
#%% fonction CRUD pour récupérer l'historique des prédictions
def get_predictions(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère l'historique des prédictions (utile pour le monitoring).
    """
    return db.query(models.PredictionRecord).offset(skip).limit(limit).all()