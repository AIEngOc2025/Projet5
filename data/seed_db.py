import requests
import pandas as pd
import time

API_URL = "http://127.0.0.1:8000/predict"

# Données d'exemple (tu peux aussi charger un vrai CSV avec pd.read_csv)
sample_data = [
    {"property_gfa_total": 2500.0, "year_built": 1985, "building_type": "Office"},
    {"property_gfa_total": 1200.5, "year_built": 2010, "building_type": "Hotel"},
    {"property_gfa_total": 5400.0, "year_built": 2022, "building_type": "Retail"},
    {"property_gfa_total": 800.0,  "year_built": 1960, "building_type": "Warehouse"},
    {"property_gfa_total": 15000.0, "year_built": 2015, "building_type": "Office"},
]

def seed_database():
    print(f"Démarrage de l'insertion vers {API_URL}...")
    
    for i, record in enumerate(sample_data):
        try:
            response = requests.post(API_URL, json=record)
            if response.status_code == 200:
                print(f"[{i+1}] Succès : {record['building_type']} enregistré.")
            else:
                print(f"[{i+1}] Échec : {response.text}")
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            break
        
        # Petite pause pour simuler un trafic réel
        time.sleep(0.5)

    print("\n🏁 Fin de l'insertion. Vérifiez votre historique sur http://127.0.0.1:8000/history")

if __name__ == "__main__":
    seed_database()