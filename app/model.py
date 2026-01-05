#%% --- IMPORTATIONS ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib


#%% --- 1. CHARGEMENT ET ENTRAÎNEMENT RAPIDE on utilsera joblib pour sauvegarder le modèle après entrainement ---    
def train_model():
    """Entraine le modèle"""
    df_sample = pd.read_csv('/Users/mpaga/Desktop/OC/Projets/Projet3/data/2016_Building_Energy_Benchmarking.csv')
    # Création de la cible et Nettoyage des données  
    df_sample = df_sample.fillna({'TotalGHGEmissions':df_sample['TotalGHGEmissions'].median()})
    df_sample['Log_TotalGHGEmissions'] = np.log1p(df_sample['TotalGHGEmissions'] + 1)
                              
    X = df_sample.drop(columns=['Log_TotalGHGEmissions'])
    y = df_sample['Log_TotalGHGEmissions']
   

    num_features = ['PropertyGFATotal', 'PropertyGFAParking', 'NumberofBuildings', 
                    'NumberofFloors', 'YearBuilt', 'ENERGYSTARScore', 
                    'SteamUse(kBtu)', 'NaturalGas(therms)', 'GHGEmissionsIntensity']
    
    cat_features = ['BuildingType', 'PrimaryPropertyType', 'CouncilDistrictCode', 
                    'Neighborhood', 'ComplianceStatus']

    preprocessor = ColumnTransformer([
        ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('std', StandardScaler())]), num_features),
        ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')), ('ohe', OneHotEncoder(handle_unknown='ignore'))]), cat_features)
    ])

    model = Pipeline([('pre', preprocessor), ('reg', GradientBoostingRegressor())])
    model.fit(X, y)
    return model

model = train_model()

#%% sauvegarde du modèle avec joblib
import joblib

# On entraîne le meilleur modèle trouvé (ex: le GBR optimisé)
best_model = model

# Sauvegarde du pipeline complet (inclut le préprocesseur + le modèle)
joblib.dump(best_model, 'model_energy.joblib', compress=3)

print("Modèle compressé et sauvegardé sous 'model_energy.joblib'")




# %%
