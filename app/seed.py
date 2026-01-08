import pandas as pd
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, PredictionRecord

def seed_database():
    # 1. S'assurer que les tables existent avant l'import
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    file_path = '2016_Building_Energy_Benchmarking.csv'
    
    if not os.path.exists(file_path):
        print(f"❌ Erreur : Le fichier {file_path} est introuvable.")
        return

    print(f"📖 Lecture du fichier {file_path}...")
    df = pd.read_csv(file_path)

    print("🚀 Début de l'insertion dans PostgreSQL...")
    
    try:
        count = 0
        for _, row in df.iterrows():
            # Création de l'instance de modèle
            # On mappe les colonnes CSV vers les attributs SQLAlchemy
            new_record = PredictionRecord(
                property_gfa_total = float(row.get('PropertyGFATotal', 0)),
                year_built = int(row.get('YearBuilt', 1900)),
                building_type = str(row.get('BuildingType', 'Unknown')),
                
                # On remplit les autres colonnes nécessaires au modèle ML
                property_gfa_parking = float(row.get('PropertyGFAParking', 0)),
                number_of_buildings = int(row.get('NumberofBuildings', 1)),
                number_of_floors = int(row.get('NumberofFloors', 1)),
                energy_star_score = float(row.get('ENERGYSTARScore', 50)) if pd.notna(row.get('ENERGYSTARScore')) else 50.0,
                
                # Output historique (considéré ici comme une "prédiction passée")
                prediction_value = float(row.get('TotalGHGEmissions', 0))
            )
            
            db.add(new_record)
            count += 1
            
            # Commit par lots de 100 pour optimiser les performances
            if count % 100 == 0:
                db.commit()
                print(f"✅ {count} lignes insérées...")

        db.commit() # Dernier commit pour le reste
        print(f"🏁 Terminé ! {count} enregistrements insérés avec succès.")

    except Exception as e:
        db.rollback()
        print(f"❌ Une erreur est survenue, rollback effectué : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()