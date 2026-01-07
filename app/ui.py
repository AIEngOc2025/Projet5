#%% Importation des bibliothèques nécessaires
import gradio as gr
import requests

#%% URL de votre API FastAPI (locale ou déployée)
API_URL = "http://127.0.0.1:8000/predict"

#%% Fonction de prédiction via l'API
def predict_carbon(surface, year, b_type):
    # Préparation des données pour l'API
    payload = {
        "PropertyGFATotal": surface,
        "YearBuilt": year,
        "BuildingType": b_type
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code != 200:
            print(response.json())
        if response.status_code == 200:
            res = response.json()
            return f"🌿 Prédiction : {res['prediction']} {res['unit']}"
        else:
            return f"❌ Erreur API : {response.json().get('detail', 'Inconnue')}"
    except Exception as e:
        return f"🔌 Erreur de connexion : {str(e)}"

#%% Construction de l'interface
with gr.Blocks(title="Futurisys Carbon Predictor") as demo:
    gr.Markdown("# 🏢 Futurisys : Simulateur d'Empreinte Carbone")
    gr.Markdown("Entrez les caractéristiques du bâtiment pour estimer ses émissions.")
    
    with gr.Row():
        with gr.Column():
            surface = gr.Number(label="Surface Totale (m²)", value=1000)
            year = gr.Slider(minimum=1900, maximum=2025, step=1, label="Année de construction", value=2000)
            b_type = gr.Dropdown(
                choices=["Hotel", "Office", "Retail", "Warehouse"], 
                label="Type de bâtiment", 
                value="Office"
            )
            btn = gr.Button("Estimer l'empreinte", variant="primary")
        
        with gr.Column():
            output = gr.Textbox(label="Résultat")

    btn.click(fn=predict_carbon, inputs=[surface, year, b_type], outputs=output)

#%% Lancement de l'interface
if __name__ == "__main__":
    demo.launch(inline=True)