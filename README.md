# Futurisys - Energy & Carbon Prediction API

## Présentation du Projet

Ce Proof of Concept (POC) fournit une infrastructure robuste pour exposer un modèle de Machine Learning spécialisé dans la prédiction de l'empreinte carbone et de la consommation énergétique des bâtiments.

L'objectif est de transformer un modèle expérimental en un service de production fiable, testé et automatisé.

## Fonctionnalités Clés

- API RESTful : Développée avec FastAPI pour une performance optimale.

- Persistance des données : Chaque prédiction est archivée dans une base PostgreSQL.

- Validation stricte : Utilisation de Pydantic pour garantir l'intégrité des données entrantes.

- Interface Interactive : Documentation Swagger UI générée automatiquement.

- CI/CD : Pipeline automatisé testant le code et déployant vers Hugging Face Spaces.

## Installation et Configuration
1. Clonage et Environnement

Bash
git clone https://github.com/votre-repo/projet5.git
cd projet5
python -m venv projet5_venv
source projet5_venv/bin/activate  # MacOS/Linux
pip install -r requirements.txt
2. Base de données

L'API nécessite PostgreSQL. Configurez votre variable d'environnement :

Bash
export DATABASE_URL="postgresql://user:projet5@localhost:5432/futurisys_db"
3. Lancement

Bash
uvicorn app.main:app --reload
L'API sera accessible sur http://127.0.0.1:8000. La documentation interactive est disponible sur /docs.

## Schéma de Données

Le modèle de données assure la traçabilité complète des prédictions effectuées :

Colonne	Type	Description
id	Integer	Clé primaire unique
property_gfa_total	Float	Surface totale du bâtiment
year_built	Integer	Année de construction
building_type	String	Type d'usage (Office, Hotel, etc.)
prediction_value	Float	Résultat du modèle ML
created_at	DateTime	Horodatage automatique
🧪 Tests et Qualité
Pour garantir la fiabilité demandée, une suite de tests unitaires est intégrée.

Bash
## Lancer les tests et voir le rapport de couverture

python -m pytest --cov=app tests/

## Pipeline CI/CD

Le workflow GitHub Actions (.github/workflows/main.yml) automatise :

L'initialisation : Installation des dépendances et de PostgreSQL en environnement de test.

La validation : Exécution de Pytest avec un seuil de couverture.

Le déploiement : Mise à jour automatique du Space Hugging Face après succès des tests sur la branche main.

## Sécurité et Authentification

- Validation des schémas : Protection contre les injections de données malformées via Pydantic.

- Gestion des Secrets : Utilisation des variables d'environnement et des GitHub Secrets (HF_TOKEN) pour ne jamais exposer de clés en clair.