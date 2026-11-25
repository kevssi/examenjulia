"""
Generador de gráficas de alta resolución para la documentación oficial en PDF:
assets/reporte_videojuegos/
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

def generate_charts():
    os.makedirs("assets", exist_ok=True)
    df = pd.read_csv("data/videojuegos_ventas_procesado.csv")

    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

    # Paleta formal corporativa
    colores = {
        "Superventas Globales (Blockbusters - Alto Físico y Digital)": "#F43F5E",
        "Éxitos Digitales e Indies Virales (Alta Descarga, Bajo Físico)": "#3B82F6",
        "Coleccionables de Consola (Físico Fuerte, Digital Moderado)": "#10B981",
        "Fracasos Comerciales y Bajo Rendimiento (Ventas Bajas)": "#F59E0B"
    }

    # 1. Gráfica de Correlación (Heatmap)
    cols_corr = ["ventas_fisicas_millones", "ventas_digitales_millones", "precio_lanzamiento_usd", "calificacion_critica", "horas_juego"]
    nombres_corr = ["Ventas Físicas", "Ventas Digitales", "Precio USD", "Calificación", "Horas Juego"]
    corr = df[cols_corr].corr()

    fig, ax = plt.subplots(figsize=(6, 4.8), dpi=200)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1,
                xticklabels=nombres_corr, yticklabels=nombres_corr, cbar_kws={'shrink': 0.8}, ax=ax)
    ax.set_title("Matriz de Correlación de Atributos", fontsize=11, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig("assets/1_heatmap_correlacion.png")
    plt.close()

    # 2. Método del Codo y Silueta
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[cols_corr])
    k_vals = range(2, 9)
    inertias = []
    silhouettes = []
    for k in k_vals:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, labels))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=200)
    ax1.plot(k_vals, inertias, 'o-', color="#2563EB", linewidth=2, markersize=6)
    ax1.axvline(x=4, color="#DC2626", linestyle="--", alpha=0.8, label="K=4 Óptimo")
    ax1.set_title("Método del Codo (Inercia / SSE)", fontsize=10, fontweight="bold")
    ax1.set_xlabel("Número de Clústeres (K)")
    ax1.set_ylabel("Inercia")
    ax1.legend(loc="upper right", fontsize=8)

    ax2.plot(k_vals, silhouettes, 's-', color="#059669", linewidth=2, markersize=6)
    ax2.axvline(x=4, color="#DC2626", linestyle="--", alpha=0.8, label="K=4 (Silueta = 0.4197)")
    ax2.set_title("Coeficiente de Silueta", fontsize=10, fontweight="bold")
    ax2.set_xlabel("Número de Clústeres (K)")
    ax2.set_ylabel("Silhouette Score")
    ax2.legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    plt.savefig("assets/2_codo_silueta.png")
    plt.close()

    # 3. Proyección PCA 2D
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=200)
    for c_nom, col in colores.items():
        subset = df[df["Cluster_Nombre"] == c_nom]
        # Acortar nombre para leyenda
        short_name = c_nom.split(" (")[0]
        ax.scatter(subset["pca_x"], subset["pca_y"], color=col, label=short_name, alpha=0.75, s=35, edgecolors='none')
    ax.set_title("Proyección de Clústeres en PCA 2D (75.2% Varianza Explicada)", fontsize=10, fontweight="bold", pad=10)
    ax.set_xlabel("Componente Principal 1 (Volumen y Calidad - 49.9%)", fontsize=9)
    ax.set_ylabel("Componente Principal 2 (Canal Digital/Físico - 25.4%)", fontsize=9)
    ax.legend(loc="best", fontsize=7.5, frameon=True)
    plt.tight_layout()
    plt.savefig("assets/3_pca_clusters.png")
    plt.close()

    # 4. Boxplot de Ventas Totales por Clúster
    fig, ax = plt.subplots(figsize=(7, 4), dpi=200)
    sns.boxplot(data=df, x="Cluster_Nombre", y="ventas_totales_millones", palette=list(colores.values()), ax=ax, width=0.55)
    ax.set_title("Dispersión de Ventas Totales por Clúster (Millones de Copias)", fontsize=10, fontweight="bold", pad=10)
    ax.set_xlabel("")
    ax.set_ylabel("Ventas Totales (Millones)", fontsize=9)
    # Acortar etiquetas X
    labels_x = ["Blockbusters", "Fracasos", "Coleccionables", "Éxitos Digitales"]
    ax.set_xticklabels(labels_x, fontsize=8.5, fontweight="bold")
    plt.tight_layout()
    plt.savefig("assets/4_boxplot_ventas.png")
    plt.close()

    # 5. Dona de Proporción
    fig, ax = plt.subplots(figsize=(5.5, 4.5), dpi=200)
    counts = df["Cluster_Nombre"].value_counts()
    short_labels = [c.split(" (")[0] for c in counts.index]
    wedge_colors = [colores[c] for c in counts.index]
    wedges, texts, autotexts = ax.pie(counts.values, labels=short_labels, autopct="%1.1f%%", colors=wedge_colors,
                                      startangle=140, pctdistance=0.78, textprops={'fontsize': 8})
    centre_circle = plt.Circle((0, 0), 0.58, fc='white')
    ax.add_artist(centre_circle)
    ax.set_title("Proporción del Catálogo por Clúster", fontsize=10, fontweight="bold")
    plt.tight_layout()
    plt.savefig("assets/5_dona_proporcion.png")
    plt.close()

    print("Gráficas para reporte generadas exitosamente en assets/")

if __name__ == "__main__":
    generate_charts()
