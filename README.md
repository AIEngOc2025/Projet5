# Projet Futurisys : API de Prédiction d'Empreinte Carbone

## Présentation du Projet

Ce projet est un Proof of Concept (POC) visant à rendre opérationnel un modèle de Machine Learning capable de prédire l'empreinte carbone des bâtiments (Projet 3). L'objectif est d'exposer ce modèle via une API performante et sécurisée, avec une traçabilité complète des prédictions en base de données.

## Architecture Technique

Framework API : FastAPI (Documentation Swagger auto-générée).

Base de Données : PostgreSQL (Persistence des logs de prédiction).

Machine Learning : Scikit-Learn (Modèle de régression).

CI/CD : GitHub Actions (Tests automatisés et déploiement continu).

Tests : Pytest avec rapport de couverture pytest-cov.

## Installation et Utilisation

### 1. Prérequis

Python 3.12+

PostgreSQL (instance locale ou cloud)

Git LFS (pour le téléchargement du modèle .joblib)

### 2. Installation locale

- Cloner le dépôt
git clone https://github.com/votre-username/votre-repo.git
cd votre-repo

- Installer les dépendances
pip install -r requirements.txt

- Configurer les variables d'environnement (.env)
echo "DATABASE_URL=postgresql://user:password@localhost:5432/futurisys" > .env
echo "API_KEY=votre_cle_secrete" >> .env

### 3. Lancement de l'API

uvicorn app.main:app --reload
L'API sera accessible sur http://127.0.0.1:8000. La documentation interactive est disponible sur /docs.

## Sécurisation et Authentification

L'accès aux endpoints sensibles (comme /predict) est protégé par une API Key. Chaque requête doit inclure l'en-tête suivant : X-API-KEY: votre_cle_secrete

## tests et Qualité 

Pour garantir la fiabilité du code exigée par Futurisys, nous utilisons Pytest.

- Lancer les tests
pytest

## Générer le rapport de couverture

pytest --cov=app tests/

## Gestion des Versions

Nous suivons le Semantic Versioning. Chaque version stable est marquée par un tag Git.

v0.1.0 : Initialisation de la structure et API de base.

v1.0.0 : Intégration complète de PostgreSQL et déploiement de production.

## Contact

Freelance ML Engineer - [Votre Nom] Client : Futurisys - Contact technique : Aurélien
