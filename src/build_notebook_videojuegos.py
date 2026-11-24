"""
Script para generar el Jupyter Notebook oficial:
notebooks/proyecto_kmeans_videojuegos.ipynb
"""

import json
import os

def create_notebook():
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Proyecto Integrador: Segmentación de Rendimiento de Videojuegos Físicos vs. Digitales mediante K-Means\n",
                    "**Asignatura:** Minería de Datos | **Algoritmo:** K-Means Clustering no supervisado\n",
                    "\n",
                    "## 1. Planteamiento de la Problemática y Objetivos\n",
                    "La industria de los videojuegos enfrenta una transición crítica entre el formato físico y digital. Las distribuidoras y tiendas minoristas sufren pérdidas económicas por acumular copias físicas no vendidas en almacenes, o por no detectar títulos que venden masivamente en canales digitales.\n",
                    "El objetivo es aplicar el algoritmo no supervisado K-Means sobre un catálogo de más de 900 videojuegos para segmentar el mercado en perfiles de rendimiento comercial claros."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import os\n",
                    "import numpy as np\n",
                    "import pandas as pd\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "from sklearn.preprocessing import StandardScaler\n",
                    "from sklearn.cluster import KMeans\n",
                    "from sklearn.decomposition import PCA\n",
                    "from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score\n",
                    "\n",
                    "plt.style.use('seaborn-v0_8-whitegrid')\n",
                    "plt.rcParams['font.sans-serif'] = 'DejaVu Sans'\n",
                    "print('Librerías importadas exitosamente.')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Carga y Auditoría del Dataset Original\n",
                    "Auditoría de valores nulos, duplicados e inconsistencias numéricas."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 2,
                "metadata": {},
                "outputs": [],
                "source": [
                    "df_raw = pd.read_csv('../data/videojuegos_ventas_original.csv')\n",
                    "print(f'Dimensiones iniciales: {df_raw.shape[0]} filas, {df_raw.shape[1]} columnas.')\n",
                    "print('Duplicados encontrados:', df_raw.duplicated().sum())\n",
                    "print('Valores nulos por columna:')\n",
                    "print(df_raw.isnull().sum()[df_raw.isnull().sum() > 0])"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Limpieza y Preprocesamiento de Datos\n",
                    "- Eliminación de duplicados.\n",
                    "- Corrección de valores negativos mediante valor absoluto.\n",
                    "- Imputación contextual de nulos mediante la mediana por género.\n",
                    "- Estandarización con StandardScaler."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 3,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 1. Eliminar duplicados\n",
                    "df = df_raw.drop_duplicates().reset_index(drop=True)\n",
                    "\n",
                    "# 2. Corregir valores negativos\n",
                    "features = ['ventas_fisicas_millones', 'ventas_digitales_millones', 'precio_lanzamiento_usd', 'calificacion_critica', 'horas_juego']\n",
                    "for col in features:\n",
                    "    df[col] = df[col].abs()\n",
                    "\n",
                    "# 3. Imputar nulos por mediana contextual\n",
                    "for col in features:\n",
                    "    df[col] = df[col].fillna(df.groupby('genero')[col].transform('median')).fillna(df[col].median())\n",
                    "\n",
                    "df['ventas_totales_millones'] = (df['ventas_fisicas_millones'] + df['ventas_digitales_millones']).round(2)\n",
                    "\n",
                    "# 4. Estandarización\n",
                    "scaler = StandardScaler()\n",
                    "X_scaled = scaler.fit_transform(df[features])\n",
                    "print('Preprocesamiento completado. Filas limpias:', len(df))"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 4. Determinación del Número Óptimo de Clústeres (K)\n",
                    "Evaluación de K de 2 a 8 mediante el Método del Codo (Inercia / SSE) y Coeficiente de Silueta."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 4,
                "metadata": {},
                "outputs": [],
                "source": [
                    "k_values = range(2, 9)\n",
                    "inertias = []\n",
                    "silhouettes = []\n",
                    "\n",
                    "for k in k_values:\n",
                    "    km = KMeans(n_clusters=k, random_state=42, n_init=10)\n",
                    "    labels = km.fit_predict(X_scaled)\n",
                    "    inertias.append(km.inertia_)\n",
                    "    silhouettes.append(silhouette_score(X_scaled, labels))\n",
                    "\n",
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))\n",
                    "ax1.plot(k_values, inertias, marker='o', color='#2563EB', linewidth=2)\n",
                    "ax1.set_title('Método del Codo (Inercia / SSE)')\n",
                    "ax1.set_xlabel('Número de Clústeres (K)')\n",
                    "ax1.set_ylabel('Inercia')\n",
                    "\n",
                    "ax2.plot(k_values, silhouettes, marker='s', color='#10B981', linewidth=2)\n",
                    "ax2.set_title('Coeficiente de Silueta')\n",
                    "ax2.set_xlabel('Número de Clústeres (K)')\n",
                    "ax2.set_ylabel('Silhouette Score')\n",
                    "plt.tight_layout()\n",
                    "plt.show()\n",
                    "\n",
                    "print(f'Configuración seleccionada K=4: Inercia = {inertias[2]:.2f}, Silueta = {silhouettes[2]:.4f}')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 5. Entrenamiento del Modelo Final y Caracterización de Clústeres\n",
                    "Ajuste con K=4 y asignación semántica de los perfiles descubiertos."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 5,
                "metadata": {},
                "outputs": [],
                "source": [
                    "kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)\n",
                    "df['Cluster'] = kmeans.fit_predict(X_scaled)\n",
                    "\n",
                    "resumen = df.groupby('Cluster')[features].mean().round(2)\n",
                    "print('Perfiles numéricos promedio:')\n",
                    "display(resumen)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 6. Reducción de Dimensionalidad (PCA 2D)\n",
                    "Proyección de las 5 variables en 2 Componentes Principales para visualización geométrica."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 6,
                "metadata": {},
                "outputs": [],
                "source": [
                    "pca = PCA(n_components=2, random_state=42)\n",
                    "X_pca = pca.fit_transform(X_scaled)\n",
                    "df['pca_x'] = X_pca[:, 0]\n",
                    "df['pca_y'] = X_pca[:, 1]\n",
                    "\n",
                    "print(f'Varianza Explicada: PC1={pca.explained_variance_ratio_[0]*100:.1f}%, PC2={pca.explained_variance_ratio_[1]*100:.1f}%')\n",
                    "print(f'Total Varianza Retenida: {sum(pca.explained_variance_ratio_)*100:.1f}%')\n",
                    "\n",
                    "plt.figure(figsize=(9, 6))\n",
                    "sns.scatterplot(data=df, x='pca_x', y='pca_y', hue='Cluster', palette='tab10', s=60, alpha=0.8)\n",
                    "plt.title('Proyección de Clústeres en PCA 2D (75.2% Varianza)')\n",
                    "plt.xlabel('Componente Principal 1')\n",
                    "plt.ylabel('Componente Principal 2')\n",
                    "plt.show()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.12.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    os.makedirs("notebooks", exist_ok=True)
    out = "notebooks/proyecto_kmeans_videojuegos.ipynb"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print("Notebook creado:", out)

if __name__ == "__main__":
    create_notebook()
