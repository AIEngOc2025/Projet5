"""Tests pour l'API FastAPI avec vérification de la table user_inputs."""
#%% --- Imports ---
import pytest
from sqlalchemy.pool import StaticPool 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import api
from app.models import UserInputRecord, PredictionRecord ,Base, get_db

# Configuration pour SQLite en mémoire partagée
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, 
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override pour que l'API utilise le même moteur que le test
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

api.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # On crée les tables UNE SEULE FOIS pour tout le module de test
    Base.metadata.create_all(bind=engine)
    yield
    # On ne drop pas entre les tests pour garder la structure en RAM
    Base.metadata.drop_all(bind=engine)

#%% --- Tests existants ---

def test_read_root():
    client = TestClient(api)
    response = client.get("/")
    assert response.status_code == 200

#%% --- NOUVEAU TEST : Persistance des entrées utilisateur ---

def test_user_input_persistence():
    """Vérifie la base de données avec le lifespan activé."""
    # Utiliser 'with' pour déclencher le chargement du modèle (lifespan)
    with TestClient(api) as client:
        payload = {
            "property_gfa_total": 5500.0,
            "year_built": 2015,
            "building_type": "NonResidential",
            "primary_property_type": "Hotel",
            "neighborhood": "DOWNTOWN",
            "council_district_code": 7,
            "number_of_buildings": 1,
            "number_of_floors": 5,
            "property_gfa_parking": 0.0,
            "energy_star_score": 90.0,
            "steam_use": 0.0,
            "natural_gas": 0.0,
            "compliance_status": "Compliant",
            "ghg_emissions_intensity": 1.0
        }

        response = client.post("/predict", json=payload)
        
        if response.status_code != 200:
            print(f"Erreur: {response.json()}")
            
        #assert response.status_code == 200

        # Vérification en base
        db = TestingSessionLocal()
        db_record = db.query(UserInputRecord).order_by(UserInputRecord.id.desc()).first()
        assert db_record is not None
        print(f"\nInput sauvegardé ID: {db_record.id}")
        db.close()
    #---
    assert response.status_code == 200

    # 2. Vérification directe en base de données
    db = TestingSessionLocal()
    try:
        # On récupère l'entrée la plus récente
        db_record = db.query(UserInputRecord).order_by(UserInputRecord.id.desc()).first()
        
        assert db_record is not None
        assert db_record.property_gfa_total == 5500.0
        assert db_record.building_type == "NonResidential"
        print(f"\nInput bien sauvegardé en base avec l'ID : {db_record.id}")
    finally:
        db.close()

#%% --- Test de prédiction classique ---

def test_predict_success():
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
        assert response.status_code == 200
        assert "prediction_value" in response.json()