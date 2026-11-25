"""
PRÁCTICA EXAMEN - RESPUESTAS DE REGISTROS (PARTES 2, 3, 4 Y 5)
Materia: Extracción de Conocimiento en Bases de Datos
Alumno : Kevin Uriel Silva Talamantes | Grupo: TI3-9 | Maestra: Julia García
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

# Configuración para mostrar tablas completas de registros en terminal
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.precision', 2)

# Ruta del dataset original
in_path = "data/videojuegos_ventas_original.csv"
if not os.path.exists(in_path):
    in_path = "../data/videojuegos_ventas_original.csv"

# ==============================================================================================
# PARTE 2. OBTENCIÓN Y EXPLORACIÓN DEL DATASET
# ==============================================================================================
print("\n" + "=" * 95)
print(" PARTE 2. OBTENCIÓN Y EXPLORACIÓN DEL DATASET")
print("=" * 95)

# Carga del dataset original
df_raw = pd.read_csv(in_path)

print("\n>>> PRIMEROS 10 REGISTROS (df_raw.head(10)):")
print("-" * 95)
cols_vista = ["id_juego", "titulo", "genero", "plataforma", "ventas_fisicas_millones", 
              "ventas_digitales_millones", "precio_lanzamiento_usd", "calificacion_critica", "horas_juego"]
print(df_raw[cols_vista].head(10).to_string(index=True))

print("\n>>> DIMENSIONES, COLUMNAS Y TIPOS DE DATOS (df_raw.shape & df_raw.dtypes):")
print("-" * 95)
print(f"Dimensiones: {df_raw.shape[0]} filas x {df_raw.shape[1]} columnas\n")
print(df_raw.dtypes.to_string())

print("\n>>> ESTADÍSTICAS DESCRIPTIVAS DE LOS REGISTROS (df_raw.describe()):")
print("-" * 95)
print(df_raw.describe().to_string())

print("\n>>> VALORES NULOS Y REGISTROS DUPLICADOS:")
print("-" * 95)
print(f"Registros duplicados: {df_raw.duplicated().sum()}")
print("\nValores nulos por columna:")
print(df_raw.isnull().sum().to_string())

# ==============================================================================================
# PARTE 3. LIMPIEZA Y PREPARACIÓN DE DATOS
# ==============================================================================================
print("\n" + "=" * 95)
print(" PARTE 3. LIMPIEZA Y PREPARACIÓN DE DATOS")
print("=" * 95)

df_clean = df_raw.copy()
vars_num = ["ventas_fisicas_millones", "ventas_digitales_millones", 
            "precio_lanzamiento_usd", "calificacion_critica", "horas_juego"]

# 1. Eliminación de duplicados
n_dup_antes = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates().reset_index(drop=True)

# 2. Corrección de negativos (inconsistencias)
for col in vars_num:
    df_clean[col] = df_clean[col].abs()

# 3. Imputación contextual de nulos con mediana por género
for col in vars_num:
    df_clean[col] = df_clean[col].fillna(df_clean.groupby("genero")[col].transform("median"))

# 4. Cálculo de ventas totales
df_clean["ventas_totales_millones"] = (df_clean["ventas_fisicas_millones"] + df_clean["ventas_digitales_millones"]).round(2)

# 5. Escalamiento con StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clean[vars_num])

print(">>> PRIMEROS 10 REGISTROS LIMPIOS Y PREPARADOS (df_clean.head(10)):")
print("-" * 95)
print(df_clean[cols_vista].head(10).to_string(index=True))

print("\n>>> ESTADÍSTICAS DESCRIPTIVAS TRAS LA LIMPIEZA (df_clean.describe()):")
print("-" * 95)
print(df_clean[vars_num].describe().to_string())

print("\n>>> RESUMEN NUMÉRICO DE LIMPIEZA:")
print("-" * 95)
print(f"Registros iniciales     : {df_raw.shape[0]}")
print(f"Duplicados eliminados   : {n_dup_antes}")
print(f"Registros limpios finales: {df_clean.shape[0]}")
print(f"Valores nulos restantes : {df_clean[vars_num].isnull().sum().sum()}")
print(f"Valores negativos       : {(df_clean[vars_num] < 0).sum().sum()}")

# ==============================================================================================
# PARTE 4. IMPLEMENTACIÓN DEL ALGORITMO K-MEANS
# ==============================================================================================
print("\n" + "=" * 95)
print(" PARTE 4. IMPLEMENTACIÓN DEL ALGORITMO K-MEANS")
print("=" * 95)

# Evaluación de K de 2 a 8
eval_k = []
for k in range(2, 9):
    km_test = KMeans(n_clusters=k, random_state=42, n_init=10)
    lbls = km_test.fit_predict(X_scaled)
    sil = silhouette_score(X_scaled, lbls)
    eval_k.append({"K": k, "Inercia_SSE": round(km_test.inertia_, 2), "Silhouette_Score": round(sil, 4)})

df_eval = pd.DataFrame(eval_k)
print(">>> EVALUACIÓN DE 7 VALORES DE K (K=2 a K=8):")
print("-" * 95)
print(df_eval.to_string(index=False))

# Entrenamiento modelo final K=4
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_clean["Cluster"] = kmeans.fit_predict(X_scaled)

# Reducción PCA 2D
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)
df_clean["pca_x"] = X_pca[:, 0].round(3)
df_clean["pca_y"] = X_pca[:, 1].round(3)

# Mapeo de nombres
cluster_means = df_clean.groupby("Cluster")[vars_num].mean()
cluster_names = {}
for c_id, row in cluster_means.iterrows():
    fis = row["ventas_fisicas_millones"]
    dig = row["ventas_digitales_millones"]
    if fis > 5.0 and dig > 8.0:
        cluster_names[c_id] = "Superventas Globales (Blockbusters)"
    elif dig > 5.0 and fis < 3.0:
        cluster_names[c_id] = "Éxitos Digitales e Indies Virales"
    elif fis > 4.0 and dig < 5.0:
        cluster_names[c_id] = "Coleccionables de Consola (Físico Fuerte)"
    else:
        cluster_names[c_id] = "Fracasos Comerciales y Bajo Rendimiento"

df_clean["Cluster_Nombre"] = df_clean["Cluster"].map(cluster_names)

print("\n>>> CANTIDAD DE REGISTROS POR CLÚSTER:")
print("-" * 95)
conteo = df_clean["Cluster_Nombre"].value_counts()
df_conteo = pd.DataFrame({
    "Clúster": conteo.index,
    "Registros": conteo.values,
    "Porcentaje": ((conteo.values / len(df_clean)) * 100).round(1)
})
print(df_conteo.to_string(index=False))

print("\n>>> CENTROIDES OBTENIDOS (PROMEDIOS REALES POR CLÚSTER):")
print("-" * 95)
print(df_clean.groupby("Cluster_Nombre")[vars_num].mean().to_string())

# ==============================================================================================
# PARTE 5. ANÁLISIS E INTERPRETACIÓN DE RESULTADOS
# ==============================================================================================
print("\n" + "=" * 95)
print(" PARTE 5. ANÁLISIS E INTERPRETACIÓN DE RESULTADOS")
print("=" * 95)

print(">>> TABLA COMPARATIVA CONSOLIDADA DE LOS GRUPOS:")
print("-" * 95)
tabla_resumen = df_clean.groupby("Cluster_Nombre").agg(
    Registros=("id_juego", "count"),
    Vta_Fisica_Media=("ventas_fisicas_millones", "mean"),
    Vta_Digital_Media=("ventas_digitales_millones", "mean"),
    Precio_Medio=("precio_lanzamiento_usd", "mean"),
    Calif_Media=("calificacion_critica", "mean"),
    Horas_Media=("horas_juego", "mean")
).reset_index()
print(tabla_resumen.to_string(index=False))

print("\n>>> MUESTRA DE REGISTROS CON CLÚSTER ASIGNADO (PRIMEROS 15 REGISTROS):")
print("-" * 95)
cols_final = ["titulo", "genero", "plataforma", "ventas_fisicas_millones", "ventas_digitales_millones", "Cluster_Nombre"]
print(df_clean[cols_final].head(15).to_string(index=True))

print("\n" + "=" * 95)
