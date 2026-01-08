# Schéma de l'Architecture (UML simplifié)

-structure des flux :

Utilisateur ➔ saisit les données dans Gradio (UI)/doc.

UI ➔ envoie une requête JSON à FastAPI.

FastAPI ➔ valide les données avec Pydantic.

API ➔ appelle le Modèle (.joblib) pour le calcul.

API ➔ enregistre l'input + l'output dans PostgreSQL.

API ➔ renvoie le résultat à l'UI.