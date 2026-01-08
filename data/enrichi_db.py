"""Script pour enrichir la base de données via l'API FastAPI locale.
Lit un fichier CSV, prépare les payloads et envoie les requêtes POST."""
#%%
import requests
import pandas as pd
import time
import os

#%% 
API_URL = "http://127.0.0.1:8000/predict"
CSV_PATH = '/Users/mpaga/Desktop/OC/Projets/Projet3/data/2016_Building_Energy_Benchmarking.csv'

def seed_database():
    if not os.path.exists(CSV_PATH):
        print(f"Erreur : Fichier introuvable à l'adresse {CSV_PATH}")
        return

    # 1. Lecture du CSV
    print(f"Lecture du fichier CSV...")
    df = pd.read_csv(CSV_PATH)

    # 2. Préparation et insertion
    print(f"Démarrage de l'insertion vers {API_URL}...")
    
    for i, row in df.iterrows():
        # Construction du payload avec les noms normalisés (snake_case)
        # On utilise .get() pour éviter les erreurs si une colonne manque
        payload = {
            "property_gfa_total": float(row.get("PropertyGFATotal", 0)),
            "year_built": int(row.get("YearBuilt", 1900)),
            "building_type": str(row.get("BuildingType", "NonResidential")),
            
            # Caractéristiques numériques supplémentaires
            "property_gfa_parking": float(row.get("PropertyGFAParking", 0)),
            "number_of_buildings": int(row.get("NumberofBuildings", 1)),
            "number_of_floors": int(row.get("NumberofFloors", 1)),
            "energy_star_score": float(row.get("ENERGYSTARScore", 50)) if pd.notna(row.get("ENERGYSTARScore")) else 50.0,
            "steam_use": float(row.get("SteamUse(kBtu)", 0)),
            "natural_gas": float(row.get("NaturalGas(therms)", 0)),
            "ghg_intensity": float(row.get("GHGEmissionsIntensity", 0)),
            
            # Caractéristiques catégorielles supplémentaires
            "primary_property_type": str(row.get("PrimaryPropertyType", "Other")),
            "council_district_code": int(row.get("CouncilDistrictCode", 1)),
            "neighborhood": str(row.get("Neighborhood", "DOWNTOWN")),
            "compliance_status": str(row.get("ComplianceStatus", "Compliant"))
        }

        # Nettoyage des valeurs NaN résiduelles pour JSON
        payload = {k: (v if pd.notna(v) else 0) for k, v in payload.items()}

        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                print(f"[{i+1}] Succès : ID {row.get('OSEBuildingID', i)} enregistré.")
            else:
                print(f"[{i+1}] Échec : {response.status_code} - {response.text[:100]}")
        
        except Exception as e:
            print(f"Erreur de connexion critique : {e}")
            break
        
        # Pause réduite à 0.1s pour un import efficace mais stable
        time.sleep(0.1)
        
        # Sécurité pour le POC : On s'arrête à 100 lignes
        if i >= 99:
            print("\nTest de 100 lignes terminé pour validation.")
            break

    print("\n🏁 Opération terminée. Vérifiez l'historique : http://127.0.0.1:8000/history")

if __name__ == "__main__":
    seed_database()