import gradio as gr
import requests
import os

# Configuration de l'URL de l'API
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

def predict_carbon(gfa, year, btype):
    """Liaison entre l'interface et l'API"""
    payload = {
        "property_gfa_total": float(gfa),
        "year_built": int(year),
        "building_type": btype
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            pred = result.get("prediction_value", 0)
            return f"✅ Prédiction réussie\n\nRésultat : {pred:.2f} tCO2eq\nID : {result.get('id')}"
        else:
            return f"❌ Erreur API : {response.text}"
    except Exception as e:
        return f"❌ Erreur de connexion : {str(e)}"

# --- Interface avec Thème Orange ---
# On définit un thème "Soft" avec la couleur Orange en couleur primaire
custom_theme = gr.themes.Soft(
    primary_hue="orange",
    secondary_hue="slate",
    neutral_hue="slate",
).set(
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_hover="*primary_600",
)

with gr.Blocks(theme=custom_theme, title="Futurisys ML Tool") as demo:
    gr.Markdown(
        """
        # 🏢 <span style='color: #FF8C00;'>Futurisys</span> : Calculateur Carbone
        *Interface POC - Validation des modèles de Machine Learning.*
        """
    )
    
    with gr.Row():
        with gr.Column():
            gfa_input = gr.Number(label="Surface Totale (m²)", value=1500)
            year_input = gr.Slider(label="Année", minimum=1900, maximum=2026, value=2000)
            type_input = gr.Dropdown(
                label="Usage", 
                choices=["Office", "Hotel", "Retail", "Warehouse"],
                value="Office"
            )
            # Le bouton sera orange grâce au thème primary_hue
            submit_btn = gr.Button("Calculer l'empreinte", variant="primary")
        
        with gr.Column():
            output_text = gr.Textbox(label="Résultat", interactive=False, lines=4)

    submit_btn.click(fn=predict_carbon, inputs=[gfa_input, year_input, type_input], outputs=output_text)

if __name__ == "__main__":
    demo.launch(server_port=7860)