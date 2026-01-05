import os
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Récupération de l'URL (ex: postgresql://user:pass@localhost:5432/futurisys)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    # On stocke les entrées sous forme de JSON pour plus de flexibilité
    input_params = Column(JSON) 
    prediction_value = Column(Float)
    model_version = Column(String) # Important pour le POC d'Aurélien

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec succès.")

if __name__ == "__main__":
    init_db()