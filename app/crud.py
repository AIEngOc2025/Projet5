"""effectue des opérations crud sur les prédictions dans la base de données."""
from sqlalchemy.orm import Session
from . import models, schemas

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

def get_predictions(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère l'historique des prédictions (utile pour le monitoring).
    """
    return db.query(models.PredictionRecord).offset(skip).limit(limit).all()