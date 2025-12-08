
from gpt4all import GPT4All

model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf") 

promp = "Analiza el siguiente dataset de ventas de medicamentos junto con la  temperatura promedio histórica del mes en Quevedo. Identifica patrones, posibles correlaciones entre temperatura y venta de medicamentos,  y ofrece conclusiones claras para la administración de una clínica (no me des codigos ni figuras). Aquí están los datos:"

tabla = """
medicina  mes  totalventa  cantidad  temperatura
0  MEROPENEM SOLIDO PARENTERAL 1G    3       90.00         3    15.371429
1  MEROPENEM SOLIDO PARENTERAL 1G    5       15.00         1    19.000000
2  MEROPENEM SOLIDO PARENTERAL 1G    6      363.95         4    18.257143
3  MEROPENEM SOLIDO PARENTERAL 1G    7      239.50         7    14.128571
4  MEROPENEM SOLIDO PARENTERAL 1G    8      421.10         7    13.971429
5  MEROPENEM SOLIDO PARENTERAL 1G    9      767.50         8    14.257143
6  MEROPENEM SOLIDO PARENTERAL 1G   10      144.70         2    17.842857
"""

with model.chat_session():
    print(model.generate(promp + tabla, max_tokens=1024))