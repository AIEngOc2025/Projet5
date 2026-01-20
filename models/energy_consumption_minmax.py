#%%
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score
import joblib

#%% Configuration de l'expérience MLflow
mlflow.set_experiment("Futurisys_Energy_Model")

def train_model():
    """Entraine le modèle avec tracking MLflow"""
    
    # Démarrage du run MLflow
    with mlflow.start_run(run_name="GradientBoosting_Base"):
        
        # --- CHARGEMENT ---
        # Note : Utilise un chemin relatif ou une variable d'env pour la portabilité
        df_sample = pd.read_csv('/Users/mpaga/Desktop/OC/Projet3/data/2016_Building_Energy_Benchmarking.csv')
        
        # --- NETTOYAGE ---
        median_val = df_sample['TotalGHGEmissions'].median()
        df_sample = df_sample.fillna({'TotalGHGEmissions': median_val})
        df_sample['Log_TotalGHGEmissions'] = np.log1p(df_sample['TotalGHGEmissions'] + 1)
        
        X = df_sample.drop(columns=['Log_TotalGHGEmissions'])
        y = df_sample['Log_TotalGHGEmissions']

        # --- CONFIGURATION FEATURES ---
        num_features = ['PropertyGFATotal', 'PropertyGFAParking', 'NumberofBuildings', 
                        'NumberofFloors', 'YearBuilt', 'ENERGYSTARScore', 
                        'SteamUse(kBtu)', 'NaturalGas(therms)', 'GHGEmissionsIntensity']
        
        cat_features = ['BuildingType', 'PrimaryPropertyType', 'CouncilDistrictCode', 
                        'Neighborhood', 'ComplianceStatus']

        # Log des paramètres de structure
        mlflow.log_param("num_features_count", len(num_features))
        mlflow.log_param("cat_features_count", len(cat_features))
        mlflow.log_param("target", "Log_TotalGHGEmissions")

        # --- PIPELINE ---
        preprocessor = ColumnTransformer([
            ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('std', StandardScaler())]), num_features),
            ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')), ('ohe', OneHotEncoder(handle_unknown='ignore'))]), cat_features)
        ])

        model = Pipeline([
            ('pre', preprocessor), 
            ('reg', GradientBoostingRegressor(n_estimators=100, learning_rate=0.1))
        ])

        # --- ENTRAÎNEMENT ---
        model.fit(X, y)
        
        # --- ÉVALUATION ---
        predictions = model.predict(X)
        rmse = np.sqrt(mean_squared_error(y, predictions))
        r2 = r2_score(y, predictions)

        # Log des métriques de performance
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        # --- SAUVEGARDE VIA MLFLOW ---
        # Cette commande remplace avantageusement joblib.dump pour le tracking
        mlflow.sklearn.log_model(sk_model=model, name="model_energy_minmax",registered_model_name="model_energy_minmax")
        print(f"Modèle entraîné et loggé. RMSE: {rmse:.4f}, R2: {r2:.4f}")
        
        return model

if __name__ == "__main__":
    trained_pipeline = train_model()