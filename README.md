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
git clone https://github.com/votre-username/votre-repo.git TODO!!!
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

## intégration et Déploiement Continus (CI/CD)

Pour répondre aux exigences de Futurisys, ce projet utilise un pipeline automatisé via GitHub Actions. Ce système garantit que chaque modification du code est testée avant d'être déployée en production.

Fonctionnement du Pipeline

Le pipeline est divisé en deux étapes majeures (Jobs) :

### Vérification de Qualité (CI)

Déclenché sur chaque push (branches main et develop) et chaque Pull Request.

Actions : Installation de l'environnement, exécution des tests unitaires avec Pytest, et calcul du taux de couverture.

Objectif : Empêcher l'introduction de régressions ou de bugs.

### Déploiement Automatisé (CD)

Déclenché uniquement lors d'un push réussi sur la branche main.

Actions : Synchronisation sécurisée du code et du modèle (Git LFS) vers Hugging Face Spaces.

Objectif : Assurer que la version en ligne est toujours la version stable la plus récente.

### Surveillance et Rapports

Statut du Build : Le badge en haut de ce README indique en temps réel si le projet est "sain" (Pass) ou en erreur (Fail).

Couverture de Code : À chaque exécution, un rapport détaillé est généré. Nous visons un seuil de 80% de couverture minimale pour les composants critiques de l'API.

Gestion des Secrets : Toutes les clés (API_KEY, DB_URL, HF_TOKEN) sont stockées de manière chiffrée dans les GitHub Actions Secrets et ne sont jamais exposées dans le code source.

## Contact

Freelance ML Engineer - CM 
Client : Futurisys - Contact technique : Aurélien
