"""
Este es el archivo principal
1. Lee las ventas del csv previamente preparado
2. Lee el historial del clima previamente preparado
3. Junta los dos conjuntos de datos en una sola matriz
4. Envia la tabla con un promp predeterminado al chatbot para que lo analize
"""

import pandas as pd
from gpt4all import GPT4All

# Cargar ventas (2025)
ventas = pd.read_csv("ventas_2025.csv")

# Cargar clima histórico (2013–2019)
clima = pd.read_csv("clima_historico.csv")

# Agrupar clima por mes (promedios)
clima_promedio = clima.groupby("mes")[["temperatura"]].mean().reset_index()

# Unir ventas con clima promedio
datos_combinados = ventas.merge(clima_promedio, on="mes", how="left")

print(datos_combinados)

"""
EJEMPLO DE PROMP PARA ENVIAR A UNA IA PRE-ENTRENADA EN GPT-4ALL

Analiza el siguiente dataset de ventas de medicamentos junto con la 
temperatura promedio histórica del mes en Quevedo. Identifica patrones,
posibles correlaciones entre temperatura y venta de medicamentos, 
y ofrece conclusiones claras para la administración de una clínica (no me des codigos ni figuras).
Aquí están los datos:
<TABLA GENERADA>

"""

# enviar al chatbot

model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf")  #si es la primerva vez te lo descarga

prompt = "Analiza el siguiente dataset de ventas de medicamentos junto con la  temperatura promedio histórica del mes en Quevedo. Identifica patrones, posibles correlaciones entre temperatura y venta de medicamentos,  y ofrece conclusiones claras para la administración de una clínica (no me des codigos ni figuras). Aquí están los datos en forma de csv:"
csv_text = datos_combinados.to_csv(index=False) # el dataframe se convierte a csv para que el chatbot lo lea y entienda mejor

texto_final = prompt + "\n" + csv_text # se contatena y se da un salto de linea

# aqui tienes que esperar que cargue 
print("Preguntando al chatbot")
with model.chat_session():
    print(model.generate(texto_final + csv_text, max_tokens=1024))