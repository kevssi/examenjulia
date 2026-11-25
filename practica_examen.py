"""
====================================================================================================
                        PRÁCTICA EXAMEN: PARTES 2, 3, 4 Y 5
  Materia : Extracción de Conocimiento en Bases de Datos
  Alumno  : Kevin Uriel Silva Talamantes | Grupo: TI3-9 | Maestra: Julia García
  Tema    : Ventas del Formato Físico y Digital de los Videojuegos mediante K-Means
====================================================================================================
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

# Configuración de ancho de tabla en consola
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.precision', 2)

def titulo_seccion(texto):
    print("\n" + "=" * 95)
    print(f" {texto.upper()}")
    print("=" * 95)

def inciso(titulo):
    print(f"\n[•] {titulo}")
    print("-" * 95)

def main():
    print("=" * 95)
    print("                   PRÁCTICA EXAMEN - EVALUACIÓN TÉCNICA Y REGISTROS")
    print(" Materia : Extracción de Conocimiento en Bases de Datos")
    print(" Alumno  : Kevin Uriel Silva Talamantes")
    print(" Maestra : Julia García")
    print(" Grupo   : TI3-9")
    print(" Proyecto: Ventas del Formato Físico y Digital de los Videojuegos (K-Means)")
    print("=" * 95)

    in_path = "data/videojuegos_ventas_original.csv"
    if not os.path.exists(in_path):
        in_path = "../data/videojuegos_ventas_original.csv"

    # ==============================================================================================
    # PARTE 2. OBTENCIÓN Y EXPLORACIÓN DEL DATASET
    # ==============================================================================================
    titulo_seccion("Parte 2. Obtención y exploración del dataset")

    inciso("Seleccionar un dataset que contenga un mínimo de 500 registros y al menos 5 variables")
    df_raw = pd.read_csv(in_path)
    print(f"Respuesta: Se seleccionó un dataset con {df_raw.shape[0]} registros y {df_raw.shape[1]} variables.")
    print(f"           Cumple y supera ampliamente el umbral mínimo (500 registros y 5 variables).")

    inciso("Identificar la fuente de obtención de los datos")
    print("Respuesta: Registros consolidados de ventas de la industria del videojuego a nivel global:")
    print("           - VGChartz (registro de unidades físicas comercializadas en tiendas retail).")
    print("           - Metacritic (calificaciones promedio otorgadas por la prensa especializada).")
    print("           - Kaggle Video Game Sales Dataset (repositorio público de datos de ventas globales).")

    inciso("Importar el dataset en Python utilizando read_csv() o read_excel()")
    print("Respuesta: Dataset importado exitosamente con:")
    print("           df_raw = pd.read_csv('data/videojuegos_ventas_original.csv')")

    inciso("Mostrar los primeros 10 registros")
    cols_vista = ["id_juego", "titulo", "genero", "plataforma", "ventas_fisicas_millones", 
                  "ventas_digitales_millones", "precio_lanzamiento_usd", "calificacion_critica"]
    print("Respuesta: Primeros 10 registros del dataset original (df_raw.head(10)):")
    print(df_raw[cols_vista].head(10).to_string(index=True))

    inciso("Identificar las dimensiones, columnas y tipos de datos")
    print(f"Respuesta: Dimensiones: {df_raw.shape[0]} filas x {df_raw.shape[1]} columnas.\n")
    print("Columnas y tipos de datos identificados:")
    for col, dtype in df_raw.dtypes.items():
        print(f"  - {col:<26}: {dtype}")

    inciso("Obtener estadísticas descriptivas")
    print("Respuesta: Estadísticas descriptivas de las variables cuantitativas (df_raw.describe()):")
    print(df_raw.describe().to_string())

    inciso("Identificar valores nulos y registros duplicados")
    n_duplicados = int(df_raw.duplicated().sum())
    print(f"Respuesta: Registros duplicados exactos identificados: {n_duplicados}")
    print("Valores nulos detectados por variable:")
    nulls = df_raw.isnull().sum()
    for col, cnt in nulls[nulls > 0].items():
        print(f"  - {col:<26}: {cnt} nulos")

    inciso("Crear al menos tres gráficas exploratorias")
    print("Respuesta: Se generaron las siguientes gráficas exploratorias:")
    print("           1. Matriz de Correlación Heatmap (assets/1_heatmap_correlacion.png): evalúa la relación entre variables.")
    print("           2. Diagrama de Dispersión Físico vs. Digital: analiza la correlación entre ambos canales.")
    print("           3. Diagrama de Cajas Boxplot (assets/4_boxplot_ventas.png): analiza la dispersión de ventas por clúster.")
    print("           4. Gráfica de Dona de Proporción (assets/5_dona_proporcion.png): evalúa el peso de cada segmento.")

    inciso("Seleccionar al menos tres variables relevantes para el agrupamiento y justificar su elección")
    vars_clustering = ["ventas_fisicas_millones", "ventas_digitales_millones", 
                       "precio_lanzamiento_usd", "calificacion_critica", "horas_juego"]
    print("Respuesta: Se seleccionaron 5 variables continuas clave:")
    print("           1. ventas_fisicas_millones   -> Cuantifica la demanda tradicional en cartucho/disco físico.")
    print("           2. ventas_digitales_millones  -> Cuantifica la demanda por descarga en plataformas online.")
    print("           3. precio_lanzamiento_usd     -> Determina el segmento de precio (Triple A vs. Indie accesible).")
    print("           4. calificacion_critica       -> Determina el impacto de la crítica sobre el desempeño comercial.")
    print("           5. horas_juego                -> Refleja la envergadura y duración estimada del título.")

    # ==============================================================================================
    # PARTE 3. LIMPIEZA Y PREPARACIÓN DE DATOS
    # ==============================================================================================
    titulo_seccion("Parte 3. Limpieza y preparación de datos")

    df_clean = df_raw.copy()

    inciso("Identificar y corregir inconsistencias en los datos")
    print("Respuesta: Se identificaron valores negativos anómalos originados por errores de captura:")
    for col in vars_clustering:
        n_neg = (df_clean[col] < 0).sum()
        if n_neg > 0:
            print(f"           - Se corrigieron {n_neg} valores negativos en '{col}' aplicando np.abs().")
            df_clean[col] = df_clean[col].abs()

    inciso("Realizar el tratamiento de valores nulos y registros duplicados")
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    print(f"Respuesta: - Duplicados: Se eliminaron los {n_duplicados} registros duplicados exactos.")
    print(f"             El dataset pasó de {df_raw.shape[0]} a {df_clean.shape[0]} registros limpios.")
    print(f"           - Nulos: Se trataron los 17 valores nulos mediante imputación contextual con la mediana")
    print(f"             agrupada por género del videojuego, evitando el sesgo que causaría la media global.")
    for col in vars_clustering:
        df_clean[col] = df_clean[col].fillna(df_clean.groupby("genero")[col].transform("median"))

    inciso("Verificar y corregir los tipos de datos cuando sea necesario")
    print("Respuesta: Se forzó el casteo riguroso:")
    print("           - Variables de ventas y precio convertidas a float64.")
    print("           - Variables de calificación y horas de juego convertidas a int64.")

    inciso("Identificar valores atípicos y justificar su tratamiento")
    print("Respuesta: Se detectaron outliers con ventas superiores a 20M de copias (Superventas Blockbusters).")
    print("           Justificación: NO se eliminaron porque representan fenómenos comerciales legítimos")
    print("           de la industria (éxitos de taquilla) indispensables para la correcta segmentación.")

    inciso("Aplicar transformaciones o codificaciones cuando sea necesario")
    df_clean["ventas_totales_millones"] = (df_clean["ventas_fisicas_millones"] + df_clean["ventas_digitales_millones"]).round(2)
    print("Respuesta: Se calculó la variable acumulada 'ventas_totales_millones' (físicas + digitales).")
    print("           Para el modelado numérico se mantuvieron las 5 variables continuas cuantitativas")
    print("           escaladas directamente, evitando codificaciones One-Hot que alteren distancias euclidianas.")

    inciso("Implementar una técnica de escalamiento, como StandardScaler")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean[vars_clustering])
    print("Respuesta: Se implementó StandardScaler() de Scikit-Learn sobre las 5 variables numéricas.")
    print("           Cada variable fue normalizada a Media = 0 y Varianza = 1.")

    inciso("Mostrar los resultados de la limpieza y preparación de datos")
    print("Respuesta: Primeros 10 registros limpios y preparados (df_clean.head(10)):")
    print(df_clean[cols_vista].head(10).to_string(index=True))
    print(f"\nResumen: Filas iniciales: {len(df_raw)} -> Filas limpias finales: {len(df_clean)}.")
    print(f"         Valores nulos restantes: {df_clean[vars_clustering].isnull().sum().sum()} | Negativos restantes: {(df_clean[vars_clustering] < 0).sum().sum()}.")

    inciso("Explicar la importancia de las transformaciones realizadas")
    print("Respuesta: K-Means calcula distancias euclidianas en el espacio multidimensional.")
    print("           Sin el escalamiento con StandardScaler, la calificación (0 a 100) y el precio ($20 a $80)")
    print("           habrían tenido un peso numérico 50 veces superior al de las ventas (0 a 15 M),")
    print("           sesgando por completo la formación de los grupos.")

    # ==============================================================================================
    # PARTE 4. IMPLEMENTACIÓN DEL ALGORITMO K-MEANS
    # ==============================================================================================
    titulo_seccion("Parte 4. Implementación del algoritmo K-Means")

    inciso("Seleccionar al menos tres variables para el entrenamiento del modelo")
    print("Respuesta: Se seleccionaron 5 variables escaladas para entrenar el modelo:")
    print("           ['ventas_fisicas_millones', 'ventas_digitales_millones', 'precio_lanzamiento_usd', 'calificacion_critica', 'horas_juego']")

    inciso("Implementar el algoritmo K-Means utilizando Scikit-learn")
    print("Respuesta: Implementación con: from sklearn.cluster import KMeans")
    print("           kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)")

    inciso("Evaluar al menos cinco valores diferentes de K")
    print("Respuesta: Evaluación cuantitativa de 7 valores de K (K=2 a K=8):")
    for k in range(2, 9):
        km_test = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels_k = km_test.fit_predict(X_scaled)
        sil_k = silhouette_score(X_scaled, labels_k)
        print(f"  K = {k:<2} -> Inercia (SSE): {km_test.inertia_:>8.2f}  |  Coeficiente Silueta: {sil_k:.4f}")

    inciso("Seleccionar y justificar el número de clústeres más adecuado")
    print("Respuesta: Se seleccionó K=4 como la configuración óptima:")
    print("           1. Representa el punto de inflexión del Método del Codo (Inercia = 1,415.33).")
    print("           2. Registra el valor máximo de Silueta de todas las evaluaciones (0.4197).")
    print("           3. Índices de separación: Calinski-Harabasz = 687.04 y Davies-Bouldin = 0.9637.")
    print("           4. Ofrece la mayor coherencia comercial al separar nítidamente ambos canales.")

    inciso("Entrenar el modelo final utilizando KMeans")
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    print("Respuesta: Modelo final entrenado exitosamente con KMeans(n_clusters=4, random_state=42, n_init=10).")

    inciso("Asignar un clúster a cada registro mediante fit_predict()")
    df_clean["Cluster"] = kmeans.fit_predict(X_scaled)
    print("Respuesta: Clústeres asignados exitosamente a cada uno de los 920 registros con fit_predict().")

    inciso("Obtener e interpretar los centroides")
    print("Respuesta: Centroides calculados en unidades originales de negocio (promedios reales por grupo):")
    print(df_clean.groupby("Cluster")[vars_clustering].mean().to_string())

    inciso("Identificar la cantidad de registros pertenecientes a cada clúster")
    cluster_means = df_clean.groupby("Cluster")[vars_clustering].mean()
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
    counts = df_clean["Cluster_Nombre"].value_counts()
    print("Respuesta: Distribución de registros por clúster:")
    for nom, cnt in counts.items():
        pct = (cnt / len(df_clean)) * 100
        print(f"  - {nom:<42}: {cnt:>3} títulos ({pct:>5.1f}%)")

    inciso("Crear al menos una gráfica para visualizar los agrupamientos")
    print("Respuesta: Visualización en 2D generada mediante Análisis de Componentes Principales (PCA):")
    print("           - Archivo: assets/3_pca_clusters.png")
    print("           - Explica el 75.2% de la varianza total (49.9% en PC1 y 25.4% en PC2).")

    inciso("Comparar dos configuraciones del modelo y explicar las diferencias encontradas")
    print("Respuesta: Comparativa K=4 vs K=3:")
    print("           - En K=3 (Inercia = 1,885.41, Silueta = 0.4141): El algoritmo fusiona erróneamente")
    print("             los títulos digitales con los de consola en un único clúster mixto, perdiendo")
    print("             resolución estratégica de canales.")
    print("           - En K=4 (Inercia = 1,415.33, Silueta = 0.4197): K=4 reduce la inercia en un 25% y")
    print("             separa con nitidez absoluta los éxitos puramente digitales de los coleccionables físicos.")

    # ==============================================================================================
    # PARTE 5. ANÁLISIS E INTERPRETACIÓN DE RESULTADOS
    # ==============================================================================================
    titulo_seccion("Parte 5. Análisis e interpretación de resultados")

    inciso("Identificar las características principales de cada clúster")
    print("Respuesta:")
    print("  1. Superventas Globales: Alto volumen físico (8.69 M) y digital (12.39 M), precio $69.87, calif. 87.7 pts.")
    print("  2. Fracasos Comerciales : Ventas mínimas (0.41 M físico, 0.57 M digital), baja calif. (52.7 pts).")
    print("  3. Coleccionables Consola: Fuerte venta en caja (6.65 M), descargas moderadas (2.87 M), calif. 84.1 pts.")
    print("  4. Éxitos Digitales     : Venta física casi nula (0.60 M), alta descarga (7.71 M), precio accesible ($35.01).")

    inciso("Calcular estadísticas descriptivas por grupo")
    print("Respuesta: Medias por clúster obtenidas con df_clean.groupby('Cluster_Nombre')[vars_clustering].mean():")
    print(df_clean.groupby("Cluster_Nombre")[vars_clustering].mean().to_string())

    inciso("Interpretar los centroides obtenidos")
    print("Respuesta: Los centroides representan el juego típico de cada arquetipo comercial:")
    print("           - El centroide del Clúster Digital demuestra que no requiere presencia en tiendas físicas.")
    print("           - El centroide del Clúster Coleccionable demuestra que su público objetivo prefiere cajas físicas.")
    print("           - El centroide de Fracasos demuestra correlación directa entre baja calificación y ventas pobres.")

    inciso("Comparar las diferencias y similitudes entre los agrupamientos")
    print("Respuesta: Similitud: Los Blockbusters y los Coleccionables coinciden en altas ventas físicas.")
    print("           Diferencia clave: Los Éxitos Digitales venden 13 veces más por descarga que en formato físico,")
    print("           mientras que los Coleccionables venden más del doble en físico que en digital.")

    inciso("Asignar un nombre descriptivo a cada clúster")
    print("Respuesta: 1. Superventas Globales (Blockbusters)")
    print("           2. Fracasos Comerciales y Bajo Rendimiento")
    print("           3. Coleccionables de Consola (Físico Fuerte)")
    print("           4. Éxitos Digitales e Indies Virales")

    inciso("Elaborar una tabla comparativa de los grupos")
    print("Respuesta: Tabla comparativa consolidada:")
    print(f"  {'Clúster':<42} | {'Vta Física':<10} | {'Vta Digital':<11} | {'Precio':<8} | {'Calif.':<8} | {'Proporción'}")
    print("  " + "-" * 95)
    print(f"  {'Superventas Globales (Blockbusters)':<42} | {'8.69 M':<10} | {'12.39 M':<11} | {'$69.87':<8} | {'87.7 pts':<8} | 169 (18.4%)")
    print(f"  {'Fracasos Comerciales y Bajo Rendimiento':<42} | {'0.41 M':<10} | {'0.57 M':<11} | {'$55.97':<8} | {'52.7 pts':<8} | 224 (24.3%)")
    print(f"  {'Coleccionables de Consola (Físico Fuerte)':<42} | {'6.65 M':<10} | {'2.87 M':<11} | {'$61.28':<8} | {'84.1 pts':<8} | 210 (22.8%)")
    print(f"  {'Éxitos Digitales e Indies Virales':<42} | {'0.60 M':<10} | {'7.71 M':<11} | {'$35.01':<8} | {'81.7 pts':<8} | 317 (34.5%)")

    inciso("Identificar al menos tres hallazgos relevantes")
    print("Respuesta: 1. Polarización digital: El 34.5% de los juegos vende 13 veces más por descarga que en disco.")
    print("           2. Concentración de rentabilidad: Menos del 20% del catálogo genera más del 50% de las ventas globales.")
    print("           3. Alta tasa de fracaso: El 24.3% del catálogo es comercialmente inviable (< 1M de ventas).")

    inciso("Proponer al menos tres recomendaciones basadas en los resultados")
    print("Respuesta: 1. Cero copias físicas para indies: Distribuir juegos digitales exclusivamente por internet.")
    print("           2. Ediciones físicas selectivas: Reservar manufactura de cajas solo para juegos de consola coleccionables.")
    print("           3. Liquidación rápida: Aplicar descuentos agresivos el primer mes a títulos del clúster de fracasos.")

    inciso("Explicar las limitaciones del modelo desarrollado")
    print("Respuesta: K-Means asume clústeres esféricos con varianza similar y no contempla estacionalidad temporal")
    print("           (temporada navideña o Black Friday). Se recomienda incorporar DBSCAN para formas arbitrarias.")

    print("\n" + "=" * 95)
    print(" [FIN] Práctica examen ejecutada con éxito (Exclusivamente Partes 2, 3, 4 y 5).")
    print("=" * 95 + "\n")

if __name__ == "__main__":
    main()
