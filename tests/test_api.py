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
#%% --- Test de la prédiction réussie ---
def test_predict_success():
    # Utiliser "with" permet d'exécuter le lifespan et de charger le modèle
    with TestClient(api) as client:
        payload = {
            "property_gfa_total": 2000.0,
            "year_built": 1980,
            "building_type": "Office",
            "primary_property_type": "Other",
            "neighborhood": "DOWNTOWN",
            "council_district_code": 1,
            "number_of_buildings": 1,
            "number_of_floors": 1,
            "property_gfa_parking": 0.0,
            "energy_star_score": 50.0,
            "steam_use": 0.0,
            "natural_gas": 0.0,
            "compliance_status": "Compliant",
            "ghg_emissions_intensity": 0.0
        }

        response = client.post("/predict", json=payload)
        
        # Debugging si l'erreur 500 persiste
        if response.status_code != 200:
            print(f"Détail de l'erreur : {response.json()}")
                               
        assert response.status_code == 200
        data = response.json()
        
        assert "prediction_value" in data
        assert data["property_gfa_total"] == 2000.0
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