"""
Script optimizado para procesar, limpiar y ejecutar K-Means sobre el dataset de ventas de videojuegos:
data/videojuegos_ventas_procesado.csv
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

def process_videojuegos_kmeans():
    in_path = "data/videojuegos_ventas_original.csv"
    if not os.path.exists(in_path):
        raise FileNotFoundError(f"No se encontró {in_path}")

    df = pd.read_csv(in_path)
    print(f"Cargando dataset original: {len(df)} filas.")

    # 1. Auditoría y Eliminación de Duplicados
    duplicados = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"- Filas duplicadas eliminadas: {duplicados}. Filas restantes: {len(df)}")

    # 2. Corrección de valores negativos
    cols_numericas = ["ventas_fisicas_millones", "ventas_digitales_millones", 
                      "precio_lanzamiento_usd", "calificacion_critica", "horas_juego"]
    for col in cols_numericas:
        if col in df.columns:
            negativos = (df[col] < 0).sum()
            if negativos > 0:
                print(f"- Corrigiendo {negativos} valores negativos en '{col}'")
                df[col] = df[col].abs()

    # 3. Imputación contextual rápida de nulos
    for col in cols_numericas:
        nulos = df[col].isnull().sum()
        if nulos > 0:
            print(f"- Imputando {nulos} valores nulos en '{col}' con mediana por género.")
            df[col] = df[col].fillna(df.groupby('genero')[col].transform('median')).fillna(df[col].median())

    # Recalcular ventas totales limpias
    df["ventas_totales_millones"] = (df["ventas_fisicas_millones"] + df["ventas_digitales_millones"]).round(2)

    # 4. Estandarización de Variables
    features = cols_numericas
    X = df[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 5. Evaluación de K (Método del Codo y Silueta)
    print("\nEvaluando K=2 a 8:")
    k_range = range(2, 9)
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        sil_k = silhouette_score(X_scaled, labels)
        print(f"  K={k} -> Inercia: {km.inertia_:.1f} | Silueta: {sil_k:.4f}")

    # Seleccionar K=4
    k_opt = 4
    kmeans = KMeans(n_clusters=k_opt, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    # Métricas oficiales de validación
    sil = silhouette_score(X_scaled, df["Cluster"])
    cal_har = calinski_harabasz_score(X_scaled, df["Cluster"])
    dav_boul = davies_bouldin_score(X_scaled, df["Cluster"])
    print(f"\nResultados K={k_opt}:")
    print(f"- Inercia (SSE): {kmeans.inertia_:.2f}")
    print(f"- Silhouette Score: {sil:.4f}")
    print(f"- Calinski-Harabasz Index: {cal_har:.2f}")
    print(f"- Davies-Bouldin Index: {dav_boul:.4f}")

    # 6. Asignación Semántica de los Clústeres
    cluster_means = df.groupby("Cluster")[features].mean()
    print("\nPromedios por Clúster:")
    print(cluster_means)

    cluster_names = {}
    for c_id, row in cluster_means.iterrows():
        fis = row["ventas_fisicas_millones"]
        dig = row["ventas_digitales_millones"]
        calif = row["calificacion_critica"]
        
        if fis > 5.0 and dig > 8.0:
            cluster_names[c_id] = "Superventas Globales (Blockbusters - Alto Físico y Digital)"
        elif dig > 5.0 and fis < 3.0:
            cluster_names[c_id] = "Éxitos Digitales e Indies Virales (Alta Descarga, Bajo Físico)"
        elif fis > 4.0 and dig < 5.0:
            cluster_names[c_id] = "Coleccionables de Consola (Físico Fuerte, Digital Moderado)"
        else:
            cluster_names[c_id] = "Fracasos Comerciales y Bajo Rendimiento (Ventas Bajas)"

    df["Cluster_Nombre"] = df["Cluster"].map(cluster_names)
    print("\nDistribución de Clústeres:")
    for cid, name in cluster_names.items():
        count = (df["Cluster"] == cid).sum()
        pct = (count / len(df)) * 100
        print(f"- Clúster {cid} ({count} juegos, {pct:.1f}%): {name}")

    # 7. Reducción de Dimensionalidad PCA (2D)
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    df["pca_x"] = np.round(X_pca[:, 0], 3)
    df["pca_y"] = np.round(X_pca[:, 1], 3)
    var_exp = pca.explained_variance_ratio_
    print(f"\nPCA Varianza explicada: PC1={var_exp[0]*100:.1f}%, PC2={var_exp[1]*100:.1f}% (Total: {sum(var_exp)*100:.1f}%)")

    # 8. Guardar Dataset Procesado
    out_path = "data/videojuegos_ventas_procesado.csv"
    df.to_csv(out_path, index=False)
    print(f"\nDataset procesado guardado exitosamente: {out_path} ({len(df)} filas)")

if __name__ == "__main__":
    process_videojuegos_kmeans()
