import gradio as gr
import requests

# URL de ton API FastAPI (assure-toi que uvicorn tourne sur ce port)
API_URL = "http://127.0.0.1:8000/predict"

def predict_carbon(gfa, year, btype):
    # CORRECTION : Les clés ici doivent correspondre EXACTEMENT à app/schemas.py
    payload = {
        "property_gfa_total": float(gfa),
        "year_built": int(year),
        "building_type": btype
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return f"Prédiction : {result['prediction_value']:.2f} tCO2eq"
        else:
            # Affiche l'erreur détaillée renvoyée par FastAPI
            return f"Erreur API ({response.status_code}) : {response.text}"
            
    except Exception as e:
        return f"Erreur de connexion : {str(e)}"

# Interface Gradio
with gr.Blocks(title="Futurisys Prediction Tool") as demo:
    gr.Markdown("Futurisys : Prédiction Carbone")
    
    with gr.Row():
        gfa_input = gr.Number(label="Surface Totale (GFA m²)", value=1000)
        year_input = gr.Number(label="Année de construction", value=2020)
        type_input = gr.Dropdown(
            label="Type de bâtiment", 
            choices=["Office", "Hotel", "Retail", "Warehouse"],
            value="Office"
        )
    
    submit_btn = gr.Button("Calculer l'empreinte")
    output = gr.Textbox(label="Résultat")

    submit_btn.click(
        fn=predict_carbon, 
        inputs=[gfa_input, year_input, type_input], 
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_port=7860)