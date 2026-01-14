# Schéma de l'Architecture (UML simplifié)
-diagramme des classes :
```mermaid
classDiagram
    class Base {
        <<SQLAlchemy>>
        +metadata
    }

    class UserInputRecord {
        +int id
        +float property_gfa_total
        +int year_built
        +string building_type
        +float ... (11 autres variables)
        +datetime created_at
    }

    class PredictionRecord {
        +int id
        +float prediction_value
        +datetime created_at
        +int user_input_id
    }

    Base <|-- UserInputRecord
    Base <|-- PredictionRecord
    UserInputRecord "1" -- "1" PredictionRecord : génère
```

-structure des flux :

Utilisateur ➔ saisit les données dans Gradio (UI)/doc.

UI ➔ envoie une requête JSON à FastAPI.

FastAPI ➔ valide les données avec Pydantic.

API ➔ appelle le Modèle (.joblib) pour le calcul.

API ➔ enregistre l'input + l'output dans PostgreSQL.

API ➔ renvoie le résultat à l'UI.

=== Diagramme des séquences/ des flux  === 
```mermaid
    autonumber
    actor User as Utilisateur (Gradio)
    participant API as FastAPI
    participant ML as Pipeline ML (14 vars)
    participant DB as PostgreSQL (Audit Log)

    User->>API: POST /predict (3 champs saisis)
    
    Note over API: Enrichissement des données :<br/>Passage de 3 à 14 variables
    
    API->>DB: crud.save_user_input (Entrée brute)
    
    API->>ML: model.predict (Vecteur complet)
    ML-->>API: Résultat (Empreinte Carbone)
    
    API->>DB: crud.create_prediction (Archivage résultat)
    DB-->>API: Confirmation
    
    API-->>User: Réponse JSON (Prédiction)
``` 
