import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ==========================================================
# PARTE 2. OBTENCIÓN Y EXPLORACIÓN DEL DATASET
# ==========================================================

# 1. Cargar el dataset
try:
    df = pd.read_csv("data/videojuegos_ventas_original.csv")
except FileNotFoundError:
    df = pd.read_csv("videojuegos_ventas_original.csv")

print("=== Datos originales del dataset ===")
print(df.head(10))

# 2. Dimensiones, columnas y tipos de datos
print("\n--- Dimensiones del dataset ---")
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

print("\n--- Columnas y tipos de datos ---")
print(df.dtypes)

# 3. Estadísticas descriptivas
print("\n--- Estadísticas descriptivas ---")
print(df.describe())

# 4. Identificar valores nulos y registros duplicados
print("\n--- Valores nulos por columna ---")
print(df.isnull().sum())

print(f"\nTotal de registros duplicados: {df.duplicated().sum()}")


# ==========================================================
# PARTE 3. LIMPIEZA Y PREPARACIÓN DE DATOS
# ==========================================================

# 5. Tratamiento de duplicados, inconsistencias y valores nulos
df_limpio = df.drop_duplicates().copy()

caracteristicas = [
    "ventas_fisicas_millones",
    "ventas_digitales_millones",
    "precio_lanzamiento_usd",
    "calificacion_critica",
    "horas_juego"
]

# Corregir valores negativos (inconsistencias)
for col in caracteristicas:
    df_limpio[col] = df_limpio[col].abs()

# Imputar valores nulos con la mediana
for col in caracteristicas:
    df_limpio[col] = df_limpio[col].fillna(df_limpio.groupby("genero")[col].transform("median"))

# Calcular ventas totales
df_limpio["ventas_totales_millones"] = (df_limpio["ventas_fisicas_millones"] + df_limpio["ventas_digitales_millones"]).round(2)

print("\n--- Resultados tras la limpieza ---")
print(f"Registros iniciales: {len(df)}")
print(f"Registros limpios finales: {len(df_limpio)}")
print(f"Valores nulos restantes: {df_limpio[caracteristicas].isnull().sum().sum()}")
print(df_limpio[caracteristicas].describe())

# 6. Escalamiento con StandardScaler
scaler = StandardScaler()
X = df_limpio[caracteristicas]
X_escalado = scaler.fit_transform(X)

print("\n--- Variables escaladas con StandardScaler (primeras 5 muestras) ---")
df_escalado = pd.DataFrame(X_escalado, columns=caracteristicas)
print(df_escalado.head(5))


# ==========================================================
# PARTE 4. IMPLEMENTACIÓN DEL ALGORITMO K-MEANS
# ==========================================================

# 7. Evaluar diferentes valores de K (Método del Codo / Inercia)
print("\n--- Evaluación de valores de K (K=2 a K=8) ---")
evaluaciones = []
for k in range(2, 9):
    km_test = KMeans(n_clusters=k, random_state=42, n_init=10)
    km_test.fit(X_escalado)
    evaluaciones.append({"K": k, "Inercia (SSE)": round(km_test.inertia_, 2)})
    print(f"K = {k} -> Inercia (SSE): {km_test.inertia_:.2f}")

# 8. Entrenar el modelo final K-Means (K=4)
modelo = KMeans(n_clusters=4, random_state=42, n_init=10)
df_limpio["Grupo"] = modelo.fit_predict(X_escalado)

print("\n--- Modelo final entrenado exitosamente con K=4 ---")
print(f"Inercia final (SSE): {modelo.inertia_:.2f}")
print(f"Número de iteraciones: {modelo.n_iter_}")


# ==========================================================
# PARTE 5. ANÁLISIS E INTERPRETACIÓN DE RESULTADOS
# ==========================================================

# 9. Asignar nombres descriptivos a cada clúster
# Calculamos los centroides en valores reales (desescalados)
centroides_reales = scaler.inverse_transform(modelo.cluster_centers_)
df_centroides = pd.DataFrame(centroides_reales, columns=caracteristicas)

mapeo_nombres = {}
for i, fila in df_centroides.iterrows():
    vf = fila["ventas_fisicas_millones"]
    vd = fila["ventas_digitales_millones"]
    if vf > 5.0 and vd > 8.0:
        mapeo_nombres[i] = "Superventas Globales (Blockbusters)"
    elif vd > 5.0 and vf < 3.0:
        mapeo_nombres[i] = "Éxitos Digitales e Indies Virales"
    elif vf > 4.0 and vd < 5.0:
        mapeo_nombres[i] = "Coleccionables de Consola (Físico Fuerte)"
    else:
        mapeo_nombres[i] = "Fracasos Comerciales y Bajo Rendimiento"

df_limpio["Clasificacion"] = df_limpio["Grupo"].map(mapeo_nombres)
df_centroides["Clasificacion"] = df_centroides.index.map(mapeo_nombres)

# 10. Centroides obtenidos (en unidades reales)
print("\n=== Centroides del modelo (Promedios reales por clúster) ===")
print(df_centroides.to_string(index=True))

# 11. Conteo de registros por clúster
print("\n=== Cantidad de videojuegos por grupo / clasificación ===")
print(df_limpio["Clasificacion"].value_counts())

# 12. Tabla comparativa de los grupos
print("\n=== Tabla comparativa de grupos (Promedios) ===")
tabla_resumen = df_limpio.groupby("Clasificacion")[caracteristicas].mean()
print(tabla_resumen.to_string())

# 13. Primeros 10 videojuegos con su clasificación asignada
print("\n=== Muestra de videojuegos con clasificación asignada ===")
cols_mostrar = ["titulo", "genero", "plataforma", "ventas_fisicas_millones", "ventas_digitales_millones", "Clasificacion"]
print(df_limpio[cols_mostrar].head(10).to_string())


# ==========================================================
# GRÁFICA DE LOS AGRUPAMIENTOS
# ==========================================================

# 14. Gráfica de dispersión con centroides (Ventas Físicas vs Ventas Digitales)
plt.figure(figsize=(10, 6))

colores = {
    "Superventas Globales (Blockbusters)": "#d7191c",
    "Éxitos Digitales e Indies Virales": "#2b83ba",
    "Coleccionables de Consola (Físico Fuerte)": "#2ca02c",
    "Fracasos Comerciales y Bajo Rendimiento": "#7f7f7f"
}

for tipo, color in colores.items():
    sub_df = df_limpio[df_limpio["Clasificacion"] == tipo]
    plt.scatter(
        sub_df["ventas_fisicas_millones"],
        sub_df["ventas_digitales_millones"],
        color=color,
        s=60,
        alpha=0.7,
        label=tipo
    )

# Centroides (proyectados en Ventas Físicas vs Ventas Digitales)
for grupo_id, nombre in mapeo_nombres.items():
    c_fis = df_centroides.loc[grupo_id, "ventas_fisicas_millones"]
    c_dig = df_centroides.loc[grupo_id, "ventas_digitales_millones"]
    plt.scatter(
        c_fis,
        c_dig,
        color="black",
        marker="X",
        s=200,
        linewidths=2,
        label="Centroides" if grupo_id == 0 else ""
    )

plt.title("Clasificación de Videojuegos con K-Means (Ventas Físicas vs Digitales)", fontsize=13, fontweight="bold")
plt.xlabel("Ventas Físicas (Millones de Copias)", fontsize=11)
plt.ylabel("Ventas Digitales (Millones de Copias)", fontsize=11)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("grafica_kmeans_videojuegos.png", dpi=300)
print("\nGráfica guardada como 'grafica_kmeans_videojuegos.png'")
plt.show()
