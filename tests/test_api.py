#%% importer les bibliothèques nécessaires
from fastapi.testclient import TestClient
from app import app
#%% creation d'un client de test
client = TestClient(app)

#%% test de l'endpoint racine
def test_prediction_endpoint():
    response = client.post("/predict", json={"Surface": 500, "YearBuilt": 2010, "PropertyType": "Office"})
    assert response.status_code == 200
    assert "prediction" in response.json()