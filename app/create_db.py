from app.database import Base, engine
from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # --- INPUTS ---
    property_gfa_total = Column(Float)
    year_built = Column(Integer)
    building_type = Column(String)
    # ... Ajoutez ici les autres colonnes parmi les 14 identifiées (Neighborhood, etc.)
    
    # --- OUTPUTS ---
    energy_prediction = Column(Float)

# Commande pour créer physiquement la table dans PostgreSQL
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Base de données et table 'predictions' créées avec succès.")