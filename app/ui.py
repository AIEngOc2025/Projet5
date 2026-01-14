import gradio as gr
import requests
import os

# Configuration de l'URL de l'API
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

def predict_carbon(gfa, year, btype):
    """
    Prépare le payload avec les 14 colonnes attendues par le backend
    tout en ne demandant que 3 infos à l'utilisateur.
    """
    # Construction du dictionnaire complet (Matching exact avec main.py)
    payload = {
        # Données dynamiques de l'UI
        "property_gfa_total": float(gfa),
        "year_built": int(year),
        "building_type": btype,
        
        # Données complétées par défaut (pour satisfaire les 14 colonnes)
        "property_gfa_parking": 0,
        "number_of_buildings": 1,
        "number_of_floors": 1,
        "energy_star_score": 50,
        "steam_use": 0,
        "natural_gas": 0,
        "ghg_intensity": 0,
        "primary_property_type": "Other",
        "council_district_code": 1,
        "neighborhood": "DOWNTOWN",
        "compliance_status": "Compliant"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            pred = result.get("prediction_value", 0)
            record_id = result.get("id", "N/A")
            return f"PRÉDICTION RÉUSSIE\n\nRésultat : {pred:.2f} tCO2eq\nID Archivage : {record_id}\n\nNote : Calcul basé sur le profil standard Futurisys."
        else:
            return f"Erreur API ({response.status_code}) : {response.text}"
            
    except Exception as e:
        return f"Erreur de connexion : {str(e)}"

# --- Interface avec Thème Orange Futurisys ---
custom_theme = gr.themes.Soft(
    primary_hue="orange",
    secondary_hue="slate",
).set(
    button_primary_background_fill="*primary_500",
)

with gr.Blocks(title="Futurisys ML Tool") as demo:
    gr.Markdown(
        """
        #<span style='color: #FF8C00;'>Futurisys</span> : Calculateur Carbone
        *Interface de démonstration POC - Validation du modèle prédictif.*
        """
    )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🛠️ Paramètres du Bâtiment")
            gfa_input = gr.Number(label="Surface Totale (m²)", value=2500)
            year_input = gr.Slider(label="Année de construction", minimum=1900, maximum=2025, value=1990, step=1)
            type_input = gr.Dropdown(
                label="Usage du Bâtiment", 
                choices=["NonResidential", "Nonresidential COS", "Multifamily LR (1-4)", "Multifamily MR (5-10)", "Campus"],
                value="NonResidential"
            )
            submit_btn = gr.Button("🚀 CALCULER L'EMPREINTE", variant="primary")
        
        with gr.Column():
            gr.Markdown("### 📊 Résultat de l'Analyse")
            output_text = gr.Textbox(label="Rapport de sortie", interactive=False, lines=10)

    submit_btn.click(
        fn=predict_carbon, 
        inputs=[gfa_input, year_input, type_input], 
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch(theme=custom_theme)