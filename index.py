"""
Aqui hacer la API, de momento con un endpoint para recibir el csv de las ventas
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from gpt4all import GPT4All

app = Flask(__name__)

# permitir peticiones desde cualquier origen (para pruebas)
CORS(app)

@app.route("/analisis", methods=["POST"])
def analisis():
    #data = request.get_json()
    #print(data)
    #nombre = data.get("nombre")
    #edad = data.get("edad")

    if "file" not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400
    
    file = request.files["file"]
    ventas = pd.read_csv(file)

    resultado =principal_analisis(ventas)
    #resultado = "CSV RECIBIDO"

    return jsonify({
        "mensaje": resultado,
    })


def principal_analisis(ventas):
    # Cargar ventas (2025)
    #ventas = pd.read_csv("Pruebas/ventas_2025.csv")

    # Cargar clima histórico (2013–2019)
    clima = pd.read_csv("Pruebas/clima_historico.csv")

    # Agrupar clima por mes (promedios)
    clima_promedio = clima.groupby("mes")[["temperatura"]].mean().reset_index()

    # Unir ventas con clima promedio
    datos_combinados = ventas.merge(clima_promedio, on="mes", how="left")

    print(datos_combinados)

    # enviar al chatbot

    model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf")  #si es la primerva vez te lo descarga

    prompt = "Analiza el siguiente dataset de ventas de medicamentos junto con la  temperatura promedio histórica del mes en Quevedo. Identifica patrones, posibles correlaciones entre temperatura y venta de medicamentos,  y ofrece conclusiones claras para la administración de una clínica (no me des codigos ni figuras). Aquí están los datos en forma de csv:"
    csv_text = datos_combinados.to_csv(index=False) # el dataframe se convierte a csv para que el chatbot lo lea y entienda mejor

    texto_final = prompt + "\n" + csv_text # se contatena y se da un salto de linea

    # aqui tienes que esperar que cargue 
    print("Preguntando al chatbot")

    respuesta = ""
    with model.chat_session():
        respuesta = model.generate(texto_final + csv_text, max_tokens=1024)
    
    return respuesta


if __name__ == "__main__":
    app.run(debug=True)
