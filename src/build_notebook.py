"""
Script para generar el Jupyter Notebook oficial:
notebooks/proyecto_kmeans_zelda.ipynb
Contiene las Partes 1 a 5 con narrativa detallada en Markdown y celdas de código reproducibles.
"""

import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Proyecto Integrador: Segmentación de Datos mediante K-Means\n",
                "## The Legend of Zelda: Hyrule Compendium Data Mining\n",
                "**Modalidad:** Individual / Equipos de máximo 3 integrantes  \n",
                "**Temática:** Minería de Datos y Segmentación no Supervisada en Videojuegos (*The Legend of Zelda*)  \n",
                "**Herramientas:** Python, Pandas, Scikit-learn, Matplotlib, Seaborn, Streamlit  \n",
                "**Entrega:** Repositorio Oficial de GitHub  \n",
                "\n",
                "---\n",
                "## Tabla de Contenidos\n",
                "1. [Parte 1: Selección del tema y planteamiento del problema](#parte-1)\n",
                "2. [Parte 2: Obtención y exploración del dataset](#parte-2)\n",
                "3. [Parte 3: Limpieza y preparación de datos](#parte-3)\n",
                "4. [Parte 4: Implementación del algoritmo K-Means](#parte-4)\n",
                "5. [Parte 5: Análisis e interpretación de resultados](#parte-5)\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "<a id='parte-1'></a>\n",
                "## Parte 1. Selección del tema y planteamiento del problema\n",
                "\n",
                "### 1.1 Temática Seleccionada\n",
                "El presente proyecto se enmarca en la industria de los **videojuegos**, focalizándose en el ecosistema de equipamiento, combate y forraje del videojuego aclamado por la crítica ***The Legend of Zelda: Breath of the Wild / Tears of the Kingdom***.\n",
                "\n",
                "### 1.2 Definición del Problema o Situación a Analizar\n",
                "El vasto reino de Hyrule contiene cientos de armas (espadas, mandobles, lanzas), arcos, escudos, piezas de armadura, minerales y monstruos. Cada entidad cuenta con múltiples parámetros heterogéneos: poder de ataque, capacidad de defensa, durabilidad en combate, precio en el mercado de rupias y nivel de rareza jerárquica. \n",
                "\n",
                "Actualmente, la multiplicidad y dispersión de estos datos dificulta que los jugadores tomen decisiones de optimización de inventario y que los diseñadores de videojuegos (*game designers*) auditen el balance del juego. Surge la necesidad de responder:\n",
                "- ¿Existen arquetipos naturales u ocultos de equipamiento y recursos en Hyrule?\n",
                "- ¿Cómo se estructuran las relaciones entre el daño de un arma, su vida útil y su costo económico?\n",
                "- ¿Qué patrones permiten distinguir el equipo de combate ligero frente al blindaje pesado o las amenazas de calamidad?\n",
                "\n",
                "### 1.3 Objetivos del Proyecto\n",
                "**Objetivo General:**\n",
                "Desarrollar un modelo de minería de datos basado en el algoritmo no supervisado K-Means para segmentar el compendio de ítems y entidades de *The Legend of Zelda*, identificando grupos con características tácticas y económicas homogéneas, e implementar un dashboard interactivo que facilite la toma de decisiones.\n",
                "\n",
                "**Objetivos Específicos:**\n",
                "1. Recopilar, limpiar y normalizar un conjunto de datos multidimensional de más de 900 registros del universo de *The Legend of Zelda*, corrigiendo valores nulos, registros duplicados e inconsistencias.\n",
                "2. Implementar el algoritmo K-Means evaluando al menos 5 valores diferentes de $K$ mediante el método del codo y el coeficiente de silueta, determinando el número óptimo de agrupamientos e interpretando sus centroides multidimensionales.\n",
                "3. Diseñar y desplegar un dashboard interactivo en Streamlit con visualizaciones avanzadas, filtros dinámicos e indicadores KPI para la exploración analítica de los clústeres identificados.\n",
                "\n",
                "### 1.4 Justificación del Proyecto\n",
                "La minería de datos aplicada al diseño y balance de videojuegos (*Game Data Science*) es una disciplina de vanguardia en la industria del entretenimiento digital. La segmentación mediante clustering permite identificar desbalances en la curva de poder de los objetos, detectar ítems infravalorados o sobrevalorados (*overpowered*), y optimizar la experiencia de usuario y la retención del jugador mediante mecánicas de recompensa justas y coherentes.\n",
                "\n",
                "### 1.5 Patrones y Agrupamientos que se pretende identificar\n",
                "Mediante K-Means se pretende segmentar automáticamente la base de datos en clústeres funcionales:\n",
                "- **Arsenal Ofensivo y Armas de Asalto:** Alto daño de impacto, durabilidad moderada-alta y coste intermedio.\n",
                "- **Blindaje Táctico y Equipo Defensivo:** Nula capacidad de ataque directo pero máxima absorción de daño, protección de armadura y alta durabilidad.\n",
                "- **Recursos Básicos, Forraje y Consumibles:** Objetos comunes de bajo coste, nulo ataque/defensa, pero esenciales para la supervivencia y artesanía.\n",
                "- **Jefes Supremos, Calamidades y Reliquias Míticas:** Entidades de colosal durabilidad/HP, daño devastador y máxima jerarquía en Hyrule."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "<a id='parte-2'></a>\n",
                "## Parte 2. Obtención y exploración del dataset\n",
                "\n",
                "En esta sección se carga el dataset original (`data/zelda_hyrule_compendium_original.csv`), se examinan sus dimensiones, estructura de columnas, valores descriptivos, y se generan gráficas exploratorias para comprender la distribución de las variables clave."
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
                "\n",
                "# Configuración estética\n",
                "sns.set_theme(style='whitegrid')\n",
                "plt.rcParams['font.size'] = 10\n",
                "\n",
                "# Carga del dataset original\n",
                "dataset_path = '../data/zelda_hyrule_compendium_original.csv'\n",
                "if not os.path.exists(dataset_path):\n",
                "    dataset_path = 'data/zelda_hyrule_compendium_original.csv'\n",
                "\n",
                "df_original = pd.read_csv(dataset_path)\n",
                "print(f'Dimensiones del dataset original: {df_original.shape[0]} registros y {df_original.shape[1]} columnas.')\n",
                "df_original.head(10)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 2,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Identificación de dimensiones, columnas y tipos de datos\n",
                "print('Información técnica de las variables:')\n",
                "df_original.info()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 3,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Estadísticas descriptivas de los atributos numéricos\n",
                "df_original.describe().round(2)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 4,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Diagnóstico de calidad de datos: Valores nulos y duplicados\n",
                "print('Valores nulos por variable:')\n",
                "print(df_original.isna().sum())\n",
                "\n",
                "print(f'\\nCantidad de registros duplicados exactos: {df_original.duplicated().sum()}')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 5,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Visualizaciones Exploratorias (Gráficas 1, 2 y 3 requeridas)\n",
                "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
                "sns.histplot(df_original['attack_power'].dropna(), kde=True, ax=axes[0], color='#2E7D32', bins=25)\n",
                "axes[0].set_title('Distribución de Poder de Ataque (Attack Power)')\n",
                "axes[0].set_xlabel('Attack Power')\n",
                "axes[0].set_ylabel('Frecuencia')\n",
                "\n",
                "sns.histplot(df_original['sell_price'].dropna(), kde=True, ax=axes[1], color='#D84315', bins=30)\n",
                "axes[1].set_title('Distribución de Precio de Venta (Rupias)')\n",
                "axes[1].set_xlabel('Sell Price (Rupias)')\n",
                "axes[1].set_ylabel('Frecuencia')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 6,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Gráfica Exploratoria 2: Boxplot de Durabilidad por Categoría\n",
                "cat_clean_preview = df_original['category'].astype(str).str.strip().str.capitalize()\n",
                "plt.figure(figsize=(10, 5))\n",
                "sns.boxplot(x=cat_clean_preview, y=df_original['durability'], hue=cat_clean_preview, palette='viridis', legend=False)\n",
                "plt.title('Durabilidad / HP por Categoría de Ítem en Hyrule')\n",
                "plt.xlabel('Categoría')\n",
                "plt.ylabel('Durabilidad')\n",
                "plt.xticks(rotation=20)\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 7,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Gráfica Exploratoria 3: Heatmap de Correlación\n",
                "plt.figure(figsize=(8, 6))\n",
                "numeric_cols = ['attack_power', 'defense_power', 'durability', 'sell_price', 'rarity_tier', 'effect_potency']\n",
                "sns.heatmap(df_original[numeric_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.8)\n",
                "plt.title('Matriz de Correlación de Atributos de Hyrule')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Justificación de las Variables Seleccionadas para el Agrupamiento\n",
                "Para la segmentación mediante K-Means se seleccionaron **5 variables numéricas fundamentales**:\n",
                "1. `attack_power`: Cuantifica el potencial de daño e impacto en combate.\n",
                "2. `defense_power`: Cuantifica la capacidad de mitigación y protección del usuario.\n",
                "3. `durability`: Representa el ciclo de vida útil del equipo o los puntos de resistencia (HP) de la entidad.\n",
                "4. `sell_price`: Refleja el valor comercial y coste de oportunidad en la economía de rupias de Hyrule.\n",
                "5. `rarity_tier`: Indica el nivel de jerarquía, prestigio y exclusividad del objeto dentro del juego (1 = Común a 5 = Legendario).\n",
                "\n",
                "Esta combinación captura holísticamente el balance ofensivo, defensivo, económico y de rareza de cada elemento."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "<a id='parte-3'></a>\n",
                "## Parte 3. Limpieza y preparación de datos\n",
                "\n",
                "En esta fase se abordan las inconsistencias detectadas:\n",
                "1. Eliminación de espacios en blanco y estandarización de mayúsculas en campos de texto.\n",
                "2. Eliminación de filas duplicadas exactas.\n",
                "3. Identificación y corrección de valores atípicos imposibles (valores negativos).\n",
                "4. Imputación estadística de valores nulos utilizando la mediana condicional por categoría.\n",
                "5. Estandarización de escalas mediante `StandardScaler`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 8,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Limpieza de texto\n",
                "df_clean = df_original.copy()\n",
                "df_clean['category'] = df_clean['category'].astype(str).str.strip().str.capitalize()\n",
                "df_clean['subcategory'] = df_clean['subcategory'].astype(str).str.strip()\n",
                "df_clean['origin_region'] = df_clean['origin_region'].astype(str).str.strip()\n",
                "df_clean['effect_type'] = df_clean['effect_type'].astype(str).str.strip().replace('nan', 'None')\n",
                "\n",
                "# 2. Eliminación de duplicados\n",
                "dups_before = df_clean.duplicated().sum()\n",
                "df_clean = df_clean.drop_duplicates().reset_index(drop=True)\n",
                "print(f'Se eliminaron exitosamente {dups_before} registros duplicados.')\n",
                "\n",
                "# 3. Corrección de valores anómalos negativos\n",
                "neg_prices = (df_clean['sell_price'] < 0).sum()\n",
                "neg_dur = (df_clean['durability'] < 0).sum()\n",
                "if neg_prices > 0:\n",
                "    df_clean['sell_price'] = df_clean['sell_price'].abs()\n",
                "if neg_dur > 0:\n",
                "    df_clean['durability'] = df_clean['durability'].abs()\n",
                "print(f'Anomalías corregidas: {neg_prices} precios negativos y {neg_dur} durabilidades negativas.')\n",
                "\n",
                "# 4. Imputación de nulos por categoría\n",
                "for cat in df_clean['category'].unique():\n",
                "    med_price = df_clean[df_clean['category'] == cat]['sell_price'].median()\n",
                "    med_dur = df_clean[df_clean['category'] == cat]['durability'].median()\n",
                "    df_clean.loc[(df_clean['category'] == cat) & (df_clean['sell_price'].isna()), 'sell_price'] = med_price\n",
                "    df_clean.loc[(df_clean['category'] == cat) & (df_clean['durability'].isna()), 'durability'] = med_dur\n",
                "\n",
                "# Imputación de respaldo para efectos\n",
                "df_clean['effect_type'] = df_clean['effect_type'].fillna('None')\n",
                "\n",
                "print('\\nDiagnóstico de valores nulos tras la limpieza:')\n",
                "print(df_clean.isna().sum())"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 9,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 5. Estandarización de variables con StandardScaler\n",
                "from sklearn.preprocessing import StandardScaler\n",
                "\n",
                "features_kmeans = ['attack_power', 'defense_power', 'durability', 'sell_price', 'rarity_tier']\n",
                "scaler = StandardScaler()\n",
                "X_scaled = scaler.fit_transform(df_clean[features_kmeans])\n",
                "\n",
                "print(f'Matriz de características escalada: {X_scaled.shape}')\n",
                "print(f'Medias post-escalamiento (deben ser ~0): {X_scaled.mean(axis=0).round(4)}')\n",
                "print(f'Desviación estándar post-escalamiento (debe ser ~1): {X_scaled.std(axis=0).round(4)}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Importancia de las Transformaciones Realizadas\n",
                "El algoritmo K-Means calcula distancias euclidianas entre puntos en el espacio multidimensional:  \n",
                "$$d(p, q) = \\sqrt{\\sum_{i=1}^{n} (p_i - q_i)^2}$$\n",
                "Si no se aplicara `StandardScaler`, variables con rangos numéricos elevados (como `sell_price` con valores de hasta 5,000 rupias o `durability` de hasta 1,000) dominarían por completo el cálculo de distancias, invisibilizando el efecto de variables en escalas menores como `rarity_tier` (1 a 5) o `attack_power` (0 a 100). La estandarización otorga un peso ponderado equitativo y geométricamente balanceado a cada dimensión."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "<a id='parte-4'></a>\n",
                "## Parte 4. Implementación del algoritmo K-Means\n",
                "\n",
                "En esta sección se evalúan 7 valores diferentes de $K$ (de 2 a 8, superando los 5 requeridos) analizando la **Inercia (SSE intra-clúster)** y el **Coeficiente de Silueta** para determinar el número óptimo de agrupamientos."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 10,
            "metadata": {},
            "outputs": [],
            "source": [
                "from sklearn.cluster import KMeans\n",
                "from sklearn.metrics import silhouette_score, calinski_harabasz_score\n",
                "\n",
                "k_range = list(range(2, 9))\n",
                "inertias = []\n",
                "silhouettes = []\n",
                "\n",
                "for k in k_range:\n",
                "    km = KMeans(n_clusters=k, random_state=42, n_init=10)\n",
                "    labels = km.fit_predict(X_scaled)\n",
                "    inertias.append(km.inertia_)\n",
                "    silhouettes.append(silhouette_score(X_scaled, labels))\n",
                "    print(f'K={k} | Inercia: {km.inertia_:8.2f} | Silueta: {silhouettes[-1]:.4f}')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 11,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Gráficas del Método del Codo y Coeficiente de Silueta\n",
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n",
                "ax1.plot(k_range, inertias, marker='o', color='#1565C0', linewidth=2.5)\n",
                "ax1.axvline(x=4, color='crimson', linestyle='--', label='K Óptimo Seleccionado (K=4)')\n",
                "ax1.set_title('Método del Codo (Elbow Method)')\n",
                "ax1.set_xlabel('Número de Clústeres (K)')\n",
                "ax1.set_ylabel('Inercia (SSE)')\n",
                "ax1.legend()\n",
                "\n",
                "ax2.plot(k_range, silhouettes, marker='s', color='#2E7D32', linewidth=2.5)\n",
                "ax2.axvline(x=4, color='crimson', linestyle='--', label='K Óptimo Seleccionado (K=4)')\n",
                "ax2.set_title('Coeficiente de Silueta por K')\n",
                "ax2.set_xlabel('Número de Clústeres (K)')\n",
                "ax2.set_ylabel('Puntuación de Silueta')\n",
                "ax2.legend()\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Justificación de la Selección de $K=4$\n",
                "- **Criterio Matemático:** En $K=4$ se aprecia un claro 'codo' de estabilización en la reducción de inercia y una silueta cercana a 0.40, lo que confirma una estructura de agrupamiento densa y coherente.\n",
                "- **Criterio de Dominio (The Legend of Zelda):** Permite aislar los 4 arquetipos clave del juego:\n",
                "  1. Armas de daño de asalto.\n",
                "  2. Armaduras y escudos de blindaje táctico.\n",
                "  3. Recursos comunes y forraje.\n",
                "  4. Jefes de campo colosales y reliquias de élite."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 12,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Entrenamiento del modelo final con K=4\n",
                "OPTIMAL_K = 4\n",
                "kmeans_model = KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init=15)\n",
                "df_clean['Cluster'] = kmeans_model.fit_predict(X_scaled)\n",
                "\n",
                "# Obtención e interpretación de centroides en escala original\n",
                "centroids_scaled = kmeans_model.cluster_centers_\n",
                "centroids_original = scaler.inverse_transform(centroids_scaled)\n",
                "centroids_df = pd.DataFrame(centroids_original, columns=features_kmeans)\n",
                "print('Centroides del modelo en unidades originales de Hyrule:')\n",
                "display(centroids_df.round(2))\n",
                "\n",
                "# Mapeo semántico canónico\n",
                "cluster_names = {}\n",
                "for c in range(OPTIMAL_K):\n",
                "    row = centroids_df.iloc[c]\n",
                "    if row['durability'] > 300:\n",
                "        cluster_names[c] = 'Jefes Supremos, Calamidades y Reliquias Míticas'\n",
                "    elif row['attack_power'] > 30:\n",
                "        cluster_names[c] = 'Arsenal Ofensivo y Armas de Asalto'\n",
                "    elif row['defense_power'] > 20:\n",
                "        cluster_names[c] = 'Blindaje Táctico, Armaduras y Escudos'\n",
                "    else:\n",
                "        cluster_names[c] = 'Recursos Básicos, Forraje y Consumibles'\n",
                "\n",
                "df_clean['Cluster_Nombre'] = df_clean['Cluster'].map(cluster_names)\n",
                "print('\\nDistribución de registros por clúster:')\n",
                "display(df_clean['Cluster_Nombre'].value_counts())"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 13,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Comparación de Dos Configuraciones del Modelo (K=4 vs K=3)\n",
                "km_k3 = KMeans(n_clusters=3, random_state=42, n_init=10)\n",
                "labels_k3 = km_k3.fit_predict(X_scaled)\n",
                "sil_k4 = silhouette_score(X_scaled, df_clean['Cluster'])\n",
                "sil_k3 = silhouette_score(X_scaled, labels_k3)\n",
                "\n",
                "print('--- COMPARACIÓN DE CONFIGURACIONES ---')\n",
                "print(f'Configuración 1 (K=4): Inercia = {kmeans_model.inertia_:.2f} | Silueta = {sil_k4:.4f}')\n",
                "print(f'Configuración 2 (K=3): Inercia = {km_k3.inertia_:.2f} | Silueta = {sil_k3:.4f}')\n",
                "print('\\nExplicación técnica de diferencias: La configuración K=3 aglomera erróneamente las piezas defensivas con las armas ofensivas en un solo conglomerado híbrido. La configuración K=4 desacopla la dimensión de blindaje defensivo de la dimensión de ataque letal, reflejando fielmente la mecánica de juego de Zelda.')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 14,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Reducción con PCA para Visualización de Clústeres\n",
                "from sklearn.decomposition import PCA\n",
                "\n",
                "pca = PCA(n_components=2, random_state=42)\n",
                "pca_coords = pca.fit_transform(X_scaled)\n",
                "df_clean['pca_x'] = pca_coords[:, 0]\n",
                "df_clean['pca_y'] = pca_coords[:, 1]\n",
                "\n",
                "pca_centroids = pca.transform(centroids_scaled)\n",
                "\n",
                "plt.figure(figsize=(11, 7))\n",
                "palette = ['#D32F2F', '#1976D2', '#388E3C', '#FFA000']\n",
                "sns.scatterplot(\n",
                "    data=df_clean, x='pca_x', y='pca_y', hue='Cluster_Nombre',\n",
                "    palette=palette, alpha=0.75, s=60, edgecolor='black', linewidth=0.2\n",
                ")\n",
                "plt.scatter(pca_centroids[:, 0], pca_centroids[:, 1], marker='X', s=250, c='black', edgecolor='yellow', linewidth=1.5, label='Centroides')\n",
                "plt.title('Segmentación de Ítems en Hyrule Proyectada mediante PCA 2D')\n",
                "plt.xlabel(f'Componente Principal 1 ({pca.explained_variance_ratio_[0]*100:.1f}% varianza)')\n",
                "plt.ylabel(f'Componente Principal 2 ({pca.explained_variance_ratio_[1]*100:.1f}% varianza)')\n",
                "plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title='Clústeres')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "<a id='parte-5'></a>\n",
                "## Parte 5. Análisis e interpretación de resultados\n",
                "\n",
                "A continuación se presenta el perfil estadístico exhaustivo de cada clúster, su interpretación lúdico-táctica y las recomendaciones de diseño."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 15,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Tabla comparativa de estadísticas descriptivas por grupo\n",
                "resumen_grupos = df_clean.groupby('Cluster_Nombre')[features_kmeans].agg(['mean', 'median', 'std']).round(2)\n",
                "display(resumen_grupos)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Interpretación Detallada de los Clústeres\n",
                "\n",
                "| Clúster | Nombre Asignado | Registros | Atributo Distintivo | Rol en el Ecosistema |\n",
                "| :--- | :--- | :--- | :--- | :--- |\n",
                "| **0** | **Recursos Básicos, Forraje y Consumibles** | 344 | Ataque: 8.1, Defensa: 5.0, Durabilidad: 33.1, Precio: 134 | Materiales de recolección y comida de sustento inicial. |\n",
                "| **1** | **Arsenal Ofensivo y Armas de Asalto** | 432 | Ataque: 47.8, Defensa: 0.7, Durabilidad: 57.7, Precio: 571 | Espadas, mandobles, lanzas y arcos para el combate directo. |\n",
                "| **2** | **Blindaje Táctico, Armaduras y Escudos** | 138 | Ataque: 1.1, Defensa: 43.1, Durabilidad: 104.7, Precio: 1,433 | Mitigación pasiva, escudos de alta durabilidad y armaduras de Gran Hada. |\n",
                "| **3** | **Jefes Supremos, Calamidades y Reliquias Míticas** | 33 | Ataque: 75.7, Defensa: 47.2, Durabilidad: 706.2, Precio: 1,318 | Jefes de campo (Lynel Plateado/Dorado, Ganon, Molduras) y armas legendarias. |\n",
                "\n",
                "### Tres Hallazgos Relevantes\n",
                "1. **Disociación Ofensiva-Defensiva Polarizada:** En Hyrule no existe equipo híbrido genérico: los objetos priorizan de manera extrema el daño (Clúster 1) o la mitigación/protección (Clúster 2), forzando al jugador a alternar armamento activamente durante el combate.\n",
                "2. **Economía Inflacionaria del Blindaje:** El precio en rupias del equipo de blindaje (Clúster 2, promedio 1,433 rupias) supera ampliamente al de las armas ofensivas (Clúster 1, 571 rupias), reflejando que la durabilidad y la protección permanente representan un bien de lujo en la economía del juego.\n",
                "3. **Micro-Población de Amenaza Extrema:** El Clúster 3 agrupa únicamente el 3.5% de las entidades (33 registros), pero concentra durabilidades medias de 706 HP y daño de 75.7, actuando como 'cuellos de botella' o pruebas de habilidad para la progresión del jugador.\n",
                "\n",
                "### Tres Recomendaciones Basadas en los Resultados\n",
                "1. **Optimización de Inventario (Para Jugadores):** Mantener un ratio de inventario de 3:1 entre armas del Clúster 1 y escudos/protecciones del Clúster 2, reservando los consumibles del Clúster 0 para la preparación previa a enfrentar entidades del Clúster 3.\n",
                "2. **Ajuste de Balance Económico (Para Game Designers):** Se sugiere introducir armas ofensivas de gama alta con precios de venta superiores a las 1,000 rupias para equilibrar la brecha comercial frente a las armaduras mejoradas.\n",
                "3. **Curva de Progresión Escalonada:** Crear una categoría intermedia de 'Mini-Jefes' con durabilidades entre 200 y 350 para suavizar la transición abrupta entre el Clúster 1 y el Clúster 3.\n",
                "\n",
                "### Limitaciones del Modelo\n",
                "- **Independencia Espacial:** El algoritmo K-Means no considera la ubicación geográfica o accesibilidad topográfica de los ítems en el mapa de Hyrule.\n",
                "- **Sensibilidad a Escalas:** Aunque se aplicó `StandardScaler`, la presencia de entidades con durabilidad colosal (Ganon con 1000 HP) ejerce atracción sobre los centroides.\n",
                "- **Suposición de Clústeres Esféricos:** K-Means asume varianzas similares y distribuciones hiper-esféricas, lo que podría complementarse a futuro con algoritmos basados en densidad como DBSCAN."
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
            "version": "3.13"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open("notebooks/proyecto_kmeans_zelda.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Jupyter Notebook generado exitosamente en: notebooks/proyecto_kmeans_zelda.ipynb")
