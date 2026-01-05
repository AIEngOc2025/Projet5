#%% import des bibliothèques nécessaires
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

#%% configuration de la base de données
Base = declarative_base()

class PredictionLog(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    input_data = Column(String)  # JSON des entrées
    prediction_result = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# L'URL sera stockée dans les secrets GitHub
# DATABASE_URL = "postgresql://user:password@host:port/dbname"