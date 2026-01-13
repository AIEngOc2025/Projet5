# [1.1.0] - 2026-01-13

## Ajouté

- **Audit Log** : Nouvelle table `user_inputs` pour stocker les requêtes brutes avant traitement.
- **Documentation** : Création du fichier `CHANGELOG.md`.
- **Stabilité des tests** : Migration vers SQLite In-Memory avec `StaticPool` pour l'isolation des tests.

## Corrigé

- Suppression des index redondants sur les clés primaires (conflit SQLite).
- Correction du chargement du modèle ML dans l'environnement de test.

## [1.0.0] - 2025-01-10

- Version initiale du POC avec prédiction énergétique et historique simple.
