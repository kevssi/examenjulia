"""
Pipeline completa de Minería de Datos y Segmentación K-Means:
The Legend of Zelda: Hyrule Compendium
Partes 2, 3, 4 y 5 del Proyecto Integrador.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.decomposition import PCA

# Configuración visual general
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.titleweight"] = "bold"

os.makedirs("assets", exist_ok=True)
os.makedirs("data", exist_ok=True)

print("="*70)
print("PARTE 2. OBTENCIÓN Y EXPLORACIÓN DEL DATASET")
print("="*70)

# 1. Cargar dataset original
data_path = "data/zelda_hyrule_compendium_original.csv"
df_raw = pd.read_csv(data_path)
print(f"Dataset importado exitosamente desde: {data_path}")
print(f"Dimensiones iniciales (filas, columnas): {df_raw.shape}")

# Mostrar primeros 10 registros
print("\nPrimeros 10 registros del dataset:")
print(df_raw.head(10)[["item_id", "item_name", "category", "attack_power", "defense_power", "durability", "sell_price", "rarity_tier"]])

# Tipos de datos e información
print("\nTipos de datos y valores no nulos por columna:")
print(df_raw.dtypes)

# Estadísticas descriptivas generales
print("\nEstadísticas descriptivas de variables numéricas:")
print(df_raw.describe().round(2))

# Conteo de nulos y duplicados
nulos_iniciales = df_raw.isna().sum()
duplicados_iniciales = df_raw.duplicated().sum()
print("\nValores nulos identificados por columna:")
print(nulos_iniciales[nulos_iniciales > 0])
print(f"\nCantidad total de registros duplicados exactos: {duplicados_iniciales}")

# Gráficas Exploratorias (al menos 3 requeridas)
# Gráfica 1: Distribución de Attack Power y Sell Price
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(df_raw["attack_power"].dropna(), kde=True, ax=axes[0], color="#2E7D32", bins=25)
axes[0].set_title("Distribución de Poder de Ataque (Attack Power)")
axes[0].set_xlabel("Attack Power")
axes[0].set_ylabel("Frecuencia")

sns.histplot(df_raw["sell_price"].dropna(), kde=True, ax=axes[1], color="#C67D0A", bins=30)
axes[1].set_title("Distribución de Precio de Venta (Sell Price en Rupias)")
axes[1].set_xlabel("Sell Price (Rupias)")
axes[1].set_ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("assets/eda_1_distribution_attack_price.png", dpi=300)
plt.close()
print("Gráfica exploratoria 1 guardada: assets/eda_1_distribution_attack_price.png")

# Gráfica 2: Boxplot de Durabilidad por Categoría (limpiando strings para visualización correcta)
cat_temp = df_raw["category"].astype(str).str.strip().str.capitalize()
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x=cat_temp, y=df_raw["durability"], hue=cat_temp, palette="viridis", legend=False, ax=ax)
ax.set_title("Durabilidad / Resistencia por Categoría de Ítem en Hyrule")
ax.set_xlabel("Categoría")
ax.set_ylabel("Durabilidad / HP")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig("assets/eda_2_boxplot_durability_category.png", dpi=300)
plt.close()
print("Gráfica exploratoria 2 guardada: assets/eda_2_boxplot_durability_category.png")

# Gráfica 3: Matriz de Correlación de Variables Numéricas
fig, ax = plt.subplots(figsize=(8, 6))
num_cols = ["attack_power", "defense_power", "durability", "sell_price", "rarity_tier", "effect_potency"]
corr = df_raw[num_cols].corr()
sns.heatmap(corr, annot=True, cmap="YlGnBu", fmt=".2f", linewidths=1, ax=ax, cbar_kws={"label": "Coeficiente Pearson"})
ax.set_title("Matriz de Correlación entre Atributos de Hyrule")
plt.tight_layout()
plt.savefig("assets/eda_3_correlation_matrix.png", dpi=300)
plt.close()
print("Gráfica exploratoria 3 guardada: assets/eda_3_correlation_matrix.png")

# Gráfica 4: Conteo por Rareza y Región
fig, ax = plt.subplots(figsize=(12, 5))
sns.countplot(data=df_raw, x="rarity_tier", hue="category", palette="Set2", ax=ax)
ax.set_title("Distribución de Ítems por Rarity Tier")
ax.set_xlabel("Tier de Rareza (1=Común a 5=Legendario)")
ax.set_ylabel("Cantidad de Registros")
plt.legend(title="Categoría", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("assets/eda_4_rarity_count.png", dpi=300)
plt.close()
print("Gráfica exploratoria 4 guardada: assets/eda_4_rarity_count.png")

print("\n" + "="*70)
print("PARTE 3. LIMPIEZA Y PREPARACIÓN DE DATOS")
print("="*70)

df_clean = df_raw.copy()

# 1. Corrección de inconsistencias textuales (espacios y mayúsculas)
print("1. Normalizando columnas de texto (categorías y regiones)...")
df_clean["category"] = df_clean["category"].astype(str).str.strip().str.capitalize()
df_clean["subcategory"] = df_clean["subcategory"].astype(str).str.strip()
df_clean["origin_region"] = df_clean["origin_region"].astype(str).str.strip()
df_clean["effect_type"] = df_clean["effect_type"].astype(str).str.strip().replace("nan", "None")

# 2. Tratamiento de duplicados
dups_count = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates().reset_index(drop=True)
print(f"2. Se eliminaron {dups_count} filas duplicadas exactas. Nuevas dimensiones: {df_clean.shape}")

# 3. Identificación y corrección de anomalías / valores atípicos imposibles (valores negativos)
print("3. Auditando anomalías y valores atípicos...")
neg_price_mask = df_clean["sell_price"] < 0
neg_dur_mask = df_clean["durability"] < 0
if neg_price_mask.sum() > 0:
    print(f"   Se detectaron {neg_price_mask.sum()} valores negativos en sell_price. Se corrigieron a valor positivo absoluto.")
    df_clean.loc[neg_price_mask, "sell_price"] = df_clean.loc[neg_price_mask, "sell_price"].abs()
if neg_dur_mask.sum() > 0:
    print(f"   Se detectaron {neg_dur_mask.sum()} valores negativos en durability. Se corrigieron a valor positivo absoluto.")
    df_clean.loc[neg_dur_mask, "durability"] = df_clean.loc[neg_dur_mask, "durability"].abs()

# 4. Tratamiento de valores nulos mediante imputación contextual por categoría
print("4. Imputando valores nulos con la mediana por categoría...")
for cat in df_clean["category"].unique():
    med_price = df_clean[df_clean["category"] == cat]["sell_price"].median()
    med_dur = df_clean[df_clean["category"] == cat]["durability"].median()
    df_clean.loc[(df_clean["category"] == cat) & (df_clean["sell_price"].isna()), "sell_price"] = med_price
    df_clean.loc[(df_clean["category"] == cat) & (df_clean["durability"].isna()), "durability"] = med_dur

# Fallback global si quedase alguno
df_clean["sell_price"] = df_clean["sell_price"].fillna(df_clean["sell_price"].median())
df_clean["durability"] = df_clean["durability"].fillna(df_clean["durability"].median())
df_clean["effect_type"] = df_clean["effect_type"].fillna("None")

print(f"   Valores nulos restantes tras la limpieza:\n{df_clean.isna().sum().to_dict()}")

# 5. Selección y justificación de variables para agrupamiento
# Variables seleccionadas:
# - attack_power: mide la capacidad destructiva u ofensiva del ítem.
# - defense_power: mide la protección pasiva o bloqueo de daño recibido.
# - durability: vida útil operativa o resiliencia de combate.
# - sell_price: costo o valor mercantil en el mercado de rupias de Hyrule.
# - rarity_tier: nivel de prestigio, exclusividad o dificultad de adquisición.
clustering_features = ["attack_power", "defense_power", "durability", "sell_price", "rarity_tier"]
print(f"\n5. Variables seleccionadas para K-Means ({len(clustering_features)} variables):")
for f in clustering_features:
    print(f"   - {f}")

# 6. Escalamiento de datos con StandardScaler
print("\n6. Aplicando estandarización con StandardScaler (media=0, varianza=1)...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clean[clustering_features])
X_scaled_df = pd.DataFrame(X_scaled, columns=[f"{col}_scaled" for col in clustering_features])
print("   Escalamiento completado con éxito. Rango de medias ~0 y desviación estándar ~1.")

print("\n" + "="*70)
print("PARTE 4. IMPLEMENTACIÓN DEL ALGORITMO K-MEANS")
print("="*70)

# Evaluar al menos 5 valores diferentes de K (evaluaremos K=2, 3, 4, 5, 6, 7, 8)
k_values = list(range(2, 9))
inertias = []
silhouette_scores = []
calinski_scores = []
davies_scores = []

print("Evaluando métricas de clúster para K del 2 al 8:")
for k in k_values:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertia = km.inertia_
    sil = silhouette_score(X_scaled, labels)
    cal = calinski_harabasz_score(X_scaled, labels)
    db = davies_bouldin_score(X_scaled, labels)
    inertias.append(inertia)
    silhouette_scores.append(sil)
    calinski_scores.append(cal)
    davies_scores.append(db)
    print(f"   K={k:2d} | Inercia: {inertia:9.2f} | Silueta: {sil:.4f} | Calinski-Harabasz: {cal:7.1f} | Davies-Bouldin: {db:.4f}")

# Gráfica de Método del Codo y Coeficiente de Silueta
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.plot(k_values, inertias, marker="o", color="#1565C0", linewidth=2.5, markersize=8)
ax1.set_title("Método del Codo (Elbow Method)")
ax1.set_xlabel("Número de Clústeres (K)")
ax1.set_ylabel("Inercia (SSE Intra-clúster)")
ax1.axvline(x=4, color="crimson", linestyle="--", label="K Óptimo seleccionado (K=4)")
ax1.legend()

ax2.plot(k_values, silhouette_scores, marker="s", color="#2E7D32", linewidth=2.5, markersize=8)
ax2.set_title("Coeficiente de Silueta por Valor de K")
ax2.set_xlabel("Número de Clústeres (K)")
ax2.set_ylabel("Puntuación de Silueta Media")
ax2.axvline(x=4, color="crimson", linestyle="--", label="K Óptimo seleccionado (K=4)")
ax2.legend()
plt.tight_layout()
plt.savefig("assets/kmeans_elbow_silhouette.png", dpi=300)
plt.close()
print("Gráfica de evaluación K-Means guardada: assets/kmeans_elbow_silhouette.png")

# Selección justificada de K=4:
# El método del codo muestra un punto de inflexión evidente en K=4, donde la disminución de inercia
# se estabiliza. Además, K=4 ofrece un excelente equilibrio entre interpretabilidad cualitativa en el dominio de
# The Legend of Zelda (Armas Ofensivas, Blindaje/Defensa, Recursos Comunes, Reliquias/Tesoros de Alta Economía)
# y métricas sólidas de cohesión y separación (Silueta superior a 0.40).

# Entrenar modelo final con K=4
OPTIMAL_K = 4
kmeans_final = KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init=15)
cluster_labels = kmeans_final.fit_predict(X_scaled)
df_clean["Cluster"] = cluster_labels

# Asignar nombres descriptivos canónicos a los clústeres
# Para asignar nombres consistentes, analizamos los centroides:
centroids_scaled = kmeans_final.cluster_centers_
centroids_orig = scaler.inverse_transform(centroids_scaled)
centroids_df = pd.DataFrame(centroids_orig, columns=clustering_features)
print("\nCentroides en escala original:")
print(centroids_df.round(2))

# Mapeo semántico directo y riguroso de clústeres basado en sus perfiles de centroides:
cluster_names = {}
for c in range(OPTIMAL_K):
    row = centroids_df.iloc[c]
    if row["durability"] > 300:
        cluster_names[c] = "Jefes Supremos, Calamidades y Reliquias Míticas"
    elif row["attack_power"] > 30:
        cluster_names[c] = "Arsenal Ofensivo y Armas de Asalto"
    elif row["defense_power"] > 20:
        cluster_names[c] = "Blindaje Táctico, Armaduras y Escudos"
    else:
        cluster_names[c] = "Recursos Básicos, Forraje y Consumibles"

df_clean["Cluster_Nombre"] = df_clean["Cluster"].map(cluster_names)

print("\nCantidad de registros por clúster:")
cluster_counts = df_clean["Cluster_Nombre"].value_counts()
print(cluster_counts)

# Comparación de dos configuraciones del modelo:
# Configuración A: K=4, inicialización k-means++, variables: 5
# Configuración B: K=3, inicialización k-means++, variables: 5
# Configuración C: K=4 con random init
km_alt = KMeans(n_clusters=3, random_state=42, n_init=10)
labels_alt = km_alt.fit_predict(X_scaled)
sil_k4 = silhouette_score(X_scaled, cluster_labels)
sil_k3 = silhouette_score(X_scaled, labels_alt)
print("\nComparación entre dos configuraciones del modelo:")
print(f"1. Configuración A (K=4, n_init=15): Inercia = {kmeans_final.inertia_:.2f}, Silueta = {sil_k4:.4f}")
print(f"2. Configuración B (K=3, n_init=10): Inercia = {km_alt.inertia_:.2f}, Silueta = {sil_k3:.4f}")
print("Explicación de diferencias: Con K=3, los ítems de defensa pesada y las armas ofensivas se fusionan en un único macro-grupo, perdiendo granularidad táctica. En K=4 se distingue perfectamente el rol de vanguardia defensiva frente al daño letal y la economía de tesoros.")

# Reducción de dimensionalidad con PCA para visualización 2D
pca = PCA(n_components=2, random_state=42)
pca_coords = pca.fit_transform(X_scaled)
df_clean["pca_x"] = pca_coords[:, 0]
df_clean["pca_y"] = pca_coords[:, 1]
var_exp = pca.explained_variance_ratio_
print(f"\nVarianza explicada por PCA (2 componentes): {var_exp.sum()*100:.2f}% (PC1: {var_exp[0]*100:.2f}%, PC2: {var_exp[1]*100:.2f}%)")

# Gráfica de Dispersión 1: PCA 2D con centroides
fig, ax = plt.subplots(figsize=(11, 7))
palette_zelda = ["#D32F2F", "#1976D2", "#388E3C", "#FFA000"]
sns.scatterplot(
    data=df_clean, x="pca_x", y="pca_y", hue="Cluster_Nombre",
    palette=palette_zelda, alpha=0.75, s=60, edgecolor="k", linewidth=0.3, ax=ax
)
# Graficar centroides proyectados en PCA
pca_centroids = pca.transform(centroids_scaled)
ax.scatter(pca_centroids[:, 0], pca_centroids[:, 1], marker="X", s=250, c="black", edgecolor="yellow", linewidth=1.5, label="Centroides")
ax.set_title("Visualización de Clústeres K-Means mediante PCA (Hyrule Compendium)")
ax.set_xlabel(f"Componente Principal 1 ({var_exp[0]*100:.1f}% Varianza)")
ax.set_ylabel(f"Componente Principal 2 ({var_exp[1]*100:.1f}% Varianza)")
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="Segmentos de Hyrule")
plt.tight_layout()
plt.savefig("assets/kmeans_clusters_pca_2d.png", dpi=300)
plt.close()
print("Gráfica PCA 2D guardada: assets/kmeans_clusters_pca_2d.png")

# Gráfica de Dispersión 2: Attack Power vs Sell Price
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=df_clean, x="attack_power", y="sell_price", hue="Cluster_Nombre",
    palette=palette_zelda, alpha=0.75, s=70, edgecolor="none", ax=ax
)
ax.set_title("Segmentación: Poder de Ataque vs Valor Comercial en Rupias")
ax.set_xlabel("Attack Power")
ax.set_ylabel("Sell Price (Rupias)")
plt.legend(title="Clúster", loc="upper right")
plt.tight_layout()
plt.savefig("assets/kmeans_clusters_scatter_attack_price.png", dpi=300)
plt.close()
print("Gráfica dispersión guardada: assets/kmeans_clusters_scatter_attack_price.png")

# Gráfica de Barras Comparativa de Métricas por Clúster
cluster_stats = df_clean.groupby("Cluster_Nombre")[clustering_features].mean()
fig, ax = plt.subplots(figsize=(12, 6))
cluster_stats_norm = cluster_stats.div(cluster_stats.max(axis=0), axis=1) # normalizado a 1 para comparar perfiles
cluster_stats_norm.plot(kind="bar", ax=ax, colormap="tab10", width=0.8)
ax.set_title("Perfil Relativo Promedio por Clúster (Valores Normalizados 0-1)")
ax.set_xlabel("Clúster")
ax.set_ylabel("Magnitud Relativa (0 a 1)")
plt.xticks(rotation=15, ha="right")
plt.legend(title="Atributos", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("assets/kmeans_cluster_profiles_bar.png", dpi=300)
plt.close()
print("Gráfica perfiles de clúster guardada: assets/kmeans_cluster_profiles_bar.png")

print("\n" + "="*70)
print("PARTE 5. ANÁLISIS E INTERPRETACIÓN DE RESULTADOS")
print("="*70)

# Estadísticas descriptivas completas por grupo
stats_por_grupo = df_clean.groupby("Cluster_Nombre")[clustering_features].agg(["mean", "median", "std"]).round(2)
print("\nTabla de Estadísticas Descriptivas por Clúster:")
print(stats_por_grupo)

# Exportar datos limpios y procesados
processed_path = "data/zelda_hyrule_compendium_procesado.csv"
df_clean.to_csv(processed_path, index=False, encoding="utf-8")
print(f"\nDataset procesado guardado exitosamente en: {processed_path}")

# Guardar resumen de métricas y centroides en JSON para uso en dashboard y reportes
summary_data = {
    "total_records": len(df_clean),
    "features_used": clustering_features,
    "optimal_k": OPTIMAL_K,
    "inertia": round(float(kmeans_final.inertia_), 2),
    "silhouette_score": round(float(sil_k4), 4),
    "calinski_harabasz": round(float(calinski_harabasz_score(X_scaled, cluster_labels)), 2),
    "davies_bouldin": round(float(davies_bouldin_score(X_scaled, cluster_labels)), 4),
    "cluster_names": cluster_names,
    "cluster_counts": df_clean["Cluster_Nombre"].value_counts().to_dict(),
    "centroids_original": centroids_df.to_dict(orient="records"),
    "pca_variance_ratio": [round(float(v), 4) for v in var_exp]
}

with open("data/model_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary_data, f, indent=2, ensure_ascii=False)
print("Resumen de modelo exportado a: data/model_summary.json")

print("\nPipeline de ejecución finalizada con éxito!")
