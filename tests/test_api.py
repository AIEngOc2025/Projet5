"""Tests pour l'API FastAPI définie dans app/main.py."""

import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import api, predict_energy
from app.database import Base, get_db

#%% --- Configuration d'une base de données de test (SQLite en mémoire) ---
# Cela évite de polluer votre vraie base PostgreSQL pendant les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#%% On remplace la dépendance get_db par celle de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

api.dependency_overrides[get_db] = override_get_db

client = TestClient(api)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Crée les tables au début des tests
    Base.metadata.create_all(bind=engine)
    yield
    # Supprime les tables à la fin
    Base.metadata.drop_all(bind=engine)

#%% --- Les Tests ---

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_predict_success():
    # Simule un envoi de données valides
    payload = {
        # Données issues de l'utilisateur
            'property_gfa_total': 2000,
            "YearBuilt": 1980,
            "BuildingType": "Office",

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

    response = client.post("/predict", json=payload)
                           
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction_value" in data
    assert data["property_gfa_total"] == 1500.5
    assert "id" in data

#%% --- Test des erreurs ---
def test_predict_invalid_data():
    # Teste la validation Pydantic (on envoie un string au lieu d'un float)
    payload = {
        "property_gfa_total": "pas_un_nombre",
        "year_built": 1995,
        "building_type": "Office"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Erreur de validation