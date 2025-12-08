"""

Este archivo de python sirve para transferir los datos climaticos del csv
a la base de datos, estos datos climaticos han sido recopilados desde 2019 hasta 2021 que fue la ultima actualizacion
fuente: https://www.datosabiertos.gob.ec/dataset/temperatura-media-mensual/resource/53ef2c7b-46d6-49c1-8a9f-7836a4cfb7e3

"""

import pandas as pd
import psycopg2

# -------------------------
# CONFIGURACIÓN POSTGRESQL
# -------------------------
conn = psycopg2.connect(
    host="localhost",
    dbname="OrlandoApp",
    user="postgres",
    password="123456",
    port=5432
)
cursor = conn.cursor()

# -------------------------
# LEER CSV Y LIMPIAR DATOS
# -------------------------

# Lee usando punto y coma
#df = pd.read_csv("climadataset.csv", sep=";", dtype=str)
df = pd.read_csv("climadataset.csv", sep=";", dtype=str, encoding="latin1")


# Reemplazar comas por puntos para convertir a float
df = df.applymap(lambda x: x.replace(",", ".") if isinstance(x, str) else x)

# Reemplazar vacíos por 0
df = df.fillna("0")

# Convertir columnas numéricas
columnas_numericas = ["longitud2", "latitud2", "altitud", "anio", 
                      "ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]

for col in columnas_numericas:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# -------------------------
# CONVERTIR A FORMATO LONG
# -------------------------

meses = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]

df_long = df.melt(
    id_vars=["Estacion", "NombreEstacion", "longitud2", "latitud2", "altitud", "anio"],
    value_vars=meses,
    var_name="mes",
    value_name="temperatura"
)

# convertir nombre del mes a número
df_long["mes_num"] = df_long["mes"].apply(lambda x: meses.index(x) + 1)

# crear fecha YYYY-MM-01
df_long["fecha"] = pd.to_datetime(df_long["anio"].astype(int).astype(str) + "-" +
                                  df_long["mes_num"].astype(str) + "-01")

# -------------------------
# INSERTAR EN POSTGRESQL
# -------------------------

insert_query = """
    INSERT INTO clima_mensual 
    (estacion, nombre_estacion, longitud, latitud, altitud, anio, mes, temperatura, fecha)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

for index, row in df_long.iterrows():
    cursor.execute(insert_query, (
        row["Estacion"],
        row["NombreEstacion"],
        row["longitud2"],
        row["latitud2"],
        row["altitud"],
        int(row["anio"]),
        int(row["mes_num"]),
        row["temperatura"],
        row["fecha"]
    ))

conn.commit()
cursor.close()
conn.close()

print("Datos insertados correctamente en PostgreSQL.")
