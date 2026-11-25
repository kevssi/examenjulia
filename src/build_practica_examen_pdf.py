"""
Script para generar el PDF exclusivo de la Práctica Examen:
docs/Practica_Examen.pdf
Contiene ÚNICAMENTE las Partes 2, 3, 4 y 5 de la rúbrica oficial,
con tipografía Arial 12, títulos en negrita y logo oficial UTSLRC.
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class PracticaExamenPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=20, top=18, right=20)
        self.add_font("Arial", "", "C:/Windows/Fonts/arial.ttf")
        self.add_font("Arial", "B", "C:/Windows/Fonts/arialbd.ttf")

    def header(self):
        pass

    def footer(self):
        pass

    def part_title(self, num_str, title_str):
        self.ln(4)
        self.set_font("Arial", "B", 13.5)
        self.set_text_color(17, 24, 39)
        self.cell(0, 7, f"PARTE {num_str}. {title_str.upper()}", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(209, 213, 219)
        self.set_line_width(0.4)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(4)

    def item_block(self, item_title, content_text):
        self.set_font("Arial", "B", 12)
        self.set_text_color(17, 24, 39)
        self.write(5.8, f"- {item_title}\n")
        self.set_font("Arial", "", 12)
        self.set_text_color(55, 65, 81)
        self.write(5.8, f"  Respuesta: {content_text}\n\n")

def build_practica_examen_pdf():
    pdf = PracticaExamenPDF()
    pdf.alias_nb_pages()

    # =========================================================================
    # PORTADA (Con logo institucional UTSLRC)
    # =========================================================================
    pdf.add_page()
    
    logo_path = "assets/logo_utslrc.png"
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=70, y=20, w=70)
        pdf.set_y(54)
    else:
        pdf.ln(30)

    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(0, 9, "PRÁCTICA EXAMEN", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 8, "Ventas del Formato Físico y Digital de los Videojuegos", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 7, "Segmentación con Algoritmo No Supervisado K-Means (Partes 2, 3, 4 y 5)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(8)
    pdf.set_draw_color(209, 213, 219)
    pdf.set_line_width(0.5)
    pdf.line(50, pdf.get_y(), 160, pdf.get_y())

    pdf.ln(45)

    campos = [
        ("Materia", "Extracción de Conocimiento en Bases de Datos"),
        ("Alumno", "Kevin Uriel Silva Talamantes"),
        ("Maestra", "Julia García"),
        ("Grupo", "TI3-9"),
        ("Fecha", "Noviembre de 2026")
    ]

    for etiqueta, valor in campos:
        pdf.set_x(45)
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(31, 41, 55)
        pdf.cell(32, 7.5, f"{etiqueta}:", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(55, 65, 81)
        pdf.cell(0, 7.5, valor, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    # =========================================================================
    # PARTE 2. OBTENCIÓN Y EXPLORACIÓN DEL DATASET
    # =========================================================================
    pdf.add_page()
    pdf.part_title("2", "Obtención y exploración del dataset")

    pdf.item_block(
        "Seleccionar un dataset que contenga un mínimo de 500 registros y al menos 5 variables",
        "El dataset seleccionado cuenta con 928 filas y 12 columnas (supera el mínimo requerido de 500 registros y 5 variables)."
    )
    pdf.item_block(
        "Identificar la fuente de obtención de los datos",
        "Registros consolidados de ventas globales: VGChartz (unidades físicas en retail), Metacritic (calificaciones promedio de prensa especializada) y Kaggle Video Game Sales Dataset."
    )
    pdf.item_block(
        "Importar el dataset en Python utilizando read_csv() o read_excel()",
        "Importado en Python mediante: df_raw = pd.read_csv('data/videojuegos_ventas_original.csv')."
    )
    pdf.item_block(
        "Mostrar los primeros 10 registros",
        "Visualizados mediante df_raw.head(10), exponiendo id_juego, titulo, genero, plataforma, ventas_fisicas_millones, ventas_digitales_millones, precio_lanzamiento_usd y calificacion_critica."
    )
    pdf.item_block(
        "Identificar las dimensiones, columnas y tipos de datos",
        "Dimensiones: 928 filas x 12 columnas. Columnas de texto (object): id_juego, titulo, genero, plataforma, distribuidora. Columnas numéricas (float64/int64): anio_lanzamiento, ventas_fisicas_millones, ventas_digitales_millones, ventas_totales_millones, precio_lanzamiento_usd, calificacion_critica y horas_juego."
    )
    pdf.item_block(
        "Obtener estadísticas descriptivas",
        "Obtenidas con df_raw.describe(): Venta física media = 3.42 M, Venta digital media = 5.76 M, Precio medio = $52.42 USD, Calificación crítica media = 76.35 puntos, Horas de juego promedio = 31.48 horas."
    )
    pdf.item_block(
        "Identificar valores nulos y registros duplicados",
        "Se detectaron 8 registros duplicados exactos y 17 valores nulos (5 en ventas digitales, 6 en precio de lanzamiento y 6 en calificación de la crítica)."
    )
    pdf.item_block(
        "Crear al menos tres gráficas exploratorias",
        "Se crearon 4 gráficas exploratorias: 1) Matriz de correlación Heatmap (assets/1_heatmap_correlacion.png), 2) Dispersión de canales de ventas físicas vs. digitales, 3) Diagrama de cajas Boxplot por clúster (assets/4_boxplot_ventas.png) y 4) Gráfica de dona de proporciones del catálogo (assets/5_dona_proporcion.png)."
    )
    pdf.item_block(
        "Seleccionar al menos tres variables relevantes para el agrupamiento y justificar su elección",
        "Se seleccionaron 5 variables continuas: ventas_fisicas_millones y ventas_digitales_millones (definen los dos canales de distribución del mercado), precio_lanzamiento_usd (evalúa la barrera de costo comercial), calificacion_critica (mide la recepción y tracción del mercado) y horas_juego (mide la duración y cantidad de contenido)."
    )

    # =========================================================================
    # PARTE 3. LIMPIEZA Y PREPARACIÓN DE DATOS
    # =========================================================================
    pdf.add_page()
    pdf.part_title("3", "Limpieza y preparación de datos")

    pdf.item_block(
        "Identificar y corregir inconsistencias en los datos",
        "Se corrigieron valores anómalos negativos en precio y ventas físicas originados por errores de digitación, aplicando la función de valor absoluto np.abs()."
    )
    pdf.item_block(
        "Realizar el tratamiento de valores nulos y registros duplicados",
        "Se eliminaron los 8 registros duplicados exactos con drop_duplicates(), reduciendo el catálogo a 920 registros limpios. Los 17 valores nulos se imputaron mediante la mediana contextual agrupada por género del videojuego, evitando el sesgo que causaría la media global."
    )
    pdf.item_block(
        "Verificar y corregir los tipos de datos cuando sea necesario",
        "Se forzó el casteo correcto a float64 en variables continuas (ventas y precio) y a int64 en calificación y horas de juego."
    )
    pdf.item_block(
        "Identificar valores atípicos y justificar su tratamiento",
        "Se identificaron outliers legítimos en juegos con más de 20M de ventas (Superventas Blockbusters). No se eliminaron porque representan fenómenos comerciales reales indispensables para la segmentación."
    )
    pdf.item_block(
        "Aplicar transformaciones o codificaciones cuando sea necesario",
        "Se calculó la variable acumulada 'ventas_totales_millones' (físicas + digitales), se corrigieron signos con np.abs(), y para el agrupamiento se preservaron las 5 variables numéricas continuas para conservar la métrica euclidiana directa sin sobredimensionar con One-Hot Encoding."
    )
    pdf.item_block(
        "Implementar una técnica de escalamiento, como StandardScaler",
        "Se implementó StandardScaler() de Scikit-Learn, transformando las 5 variables continuas a media 0 y varianza 1."
    )
    pdf.item_block(
        "Mostrar los resultados de la limpieza y preparación de datos",
        "El dataset pasó de 928 filas con anomalías a 920 filas limpias, guardadas en data/videojuegos_ventas_procesado.csv, con 0 valores nulos y 0 valores negativos restantes."
    )
    pdf.item_block(
        "Explicar la importancia de las transformaciones realizadas",
        "K-Means calcula distancias euclidianas. Sin StandardScaler, la calificación (0 a 100) y el precio ($20 a $80) habrían tenido un peso numérico 50 veces mayor que las ventas (0 a 15 M), anulando por completo la influencia de los canales de venta en los clústeres."
    )

    # =========================================================================
    # PARTE 4. IMPLEMENTACIÓN DEL ALGORITMO K-MEANS
    # =========================================================================
    pdf.add_page()
    pdf.part_title("4", "Implementación del algoritmo K-Means")

    pdf.item_block(
        "Seleccionar al menos tres variables para el entrenamiento del modelo",
        "Se seleccionaron 5 variables escaladas: ventas_fisicas_millones, ventas_digitales_millones, precio_lanzamiento_usd, calificacion_critica y horas_juego."
    )
    pdf.item_block(
        "Implementar el algoritmo K-Means utilizando Scikit-learn",
        "Implementado con: from sklearn.cluster import KMeans; kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)."
    )
    pdf.item_block(
        "Evaluar al menos cinco valores diferentes de K",
        "Se evaluaron 7 configuraciones (K=2 a K=8): K=2 (Inercia 2,947.7, Silueta 0.3373), K=3 (Inercia 1,885.4, Silueta 0.4141), K=4 (Inercia 1,415.3, Silueta 0.4197), K=5 (Inercia 1,182.6, Silueta 0.3911), K=6 (Inercia 1,082.5, Silueta 0.3738), K=7 (Inercia 1,012.1, Silueta 0.3351), K=8 (Inercia 933.1, Silueta 0.2855)."
    )
    pdf.item_block(
        "Seleccionar y justificar el número de clústeres más adecuado",
        "Se seleccionó K=4 como la configuración óptima. En K=4 se ubica el punto de inflexión del codo (Inercia = 1,415.33), el valor máximo de Silueta (0.4197), Calinski-Harabasz de 687.04 y Davies-Bouldin de 0.9637, separando con nitidez absoluta los canales físico y digital."
    )
    pdf.item_block(
        "Entrenar el modelo final utilizando KMeans",
        "Modelo final ajustado mediante: kmeans.fit(X_scaled) con n_clusters=4."
    )
    pdf.item_block(
        "Asignar un clúster a cada registro mediante fit_predict()",
        "Clústeres asignados a los 920 registros mediante: df['Cluster'] = kmeans.fit_predict(X_scaled)."
    )
    pdf.item_block(
        "Obtener e interpretar los centroides",
        "Centroides obtenidos en unidades originales: Clúster 0 (Blockbusters: 8.69M fís, 12.39M dig, $69.99 USD, 87.7 pts), Clúster 1 (Fracasos: 0.41M fís, 0.57M dig, $55.97 USD, 52.7 pts), Clúster 2 (Coleccionables: 6.65M fís, 2.87M dig, $61.28 USD, 84.1 pts), Clúster 3 (Éxitos Digitales: 0.60M fís, 7.71M dig, $35.01 USD, 81.7 pts)."
    )
    pdf.item_block(
        "Identificar la cantidad de registros pertenecientes a cada clúster",
        "Distribución final: Clúster 3 (Éxitos Digitales) con 317 juegos (34.5%), Clúster 1 (Fracasos) con 224 juegos (24.3%), Clúster 2 (Coleccionables) con 210 juegos (22.8%) y Clúster 0 (Blockbusters) con 169 juegos (18.4%)."
    )
    pdf.item_block(
        "Crear al menos una gráfica para visualizar los agrupamientos",
        "Se implementó reducción de dimensionalidad con PCA en 2D (assets/3_pca_clusters.png), reteniendo el 75.2% de la varianza total (49.9% en PC1 y 25.4% en PC2)."
    )
    pdf.item_block(
        "Comparar dos configuraciones del modelo y explicar las diferencias encontradas",
        "Comparativa K=4 vs K=3: K=3 fusionaba erróneamente los juegos digitales y los coleccionables de consola en un único grupo mixto, impidiendo tomar decisiones sobre prensado de discos. K=4 divide ambos perfiles con precisión quirúrgica."
    )

    # =========================================================================
    # PARTE 5. ANÁLISIS E INTERPRETACIÓN DE RESULTADOS
    # =========================================================================
    pdf.add_page()
    pdf.part_title("5", "Análisis e interpretación de resultados")

    pdf.item_block(
        "Identificar las características principales de cada clúster",
        "1. Blockbusters: Máxima recaudación física y digital con precio pleno. 2. Fracasos: Desempeño comercial deficiente y mala crítica. 3. Coleccionables: Tracción física superior para consolas. 4. Éxitos Digitales: Consumo masivo por internet a precio accesible."
    )
    pdf.item_block(
        "Calcular estadísticas descriptivas por grupo",
        "Calculadas con df.groupby('Cluster_Nombre').mean() para todas las variables cuantitativas de ventas, precios, notas y duración."
    )
    pdf.item_block(
        "Interpretar los centroides obtenidos",
        "Los centroides revelan que los títulos independientes y digitales no necesitan presencia física en anaqueles para triunfar, mientras que las franquicias de consola aún requieren soporte físico para satisfacer a coleccionistas."
    )
    pdf.item_block(
        "Comparar las diferencias y similitudes entre los agrupamientos",
        "Similitud: Los Blockbusters y los Coleccionables coinciden en fuerte presencia en retail físico. Diferencia: Los Éxitos Digitales venden 13 veces más por descarga que en disco, mientras que los Coleccionables venden más del doble en disco físico que en digital."
    )
    pdf.item_block(
        "Asignar un nombre descriptivo a cada clúster",
        "Clúster 0: Superventas Globales (Blockbusters) | Clúster 1: Fracasos Comerciales y Bajo Rendimiento | Clúster 2: Coleccionables de Consola (Físico Fuerte) | Clúster 3: Éxitos Digitales e Indies Virales."
    )
    pdf.item_block(
        "Elaborar una tabla comparativa de los grupos",
        "Tabla comparativa consolidada:\n- Blockbusters: 8.69M fís | 12.39M dig | $69.87 USD | 87.7 pts | 169 juegos (18.4%)\n- Fracasos Comerciales: 0.41M fís | 0.57M dig | $55.97 USD | 52.7 pts | 224 juegos (24.3%)\n- Coleccionables Consola: 6.65M fís | 2.87M dig | $61.28 USD | 84.1 pts | 210 juegos (22.8%)\n- Éxitos Digitales: 0.60M fís | 7.71M dig | $35.01 USD | 81.7 pts | 317 juegos (34.5%)"
    )
    pdf.item_block(
        "Identificar al menos tres hallazgos relevantes",
        "1. Predominio digital: El 34.5% de los videojuegos vende 13 veces más por descarga digital que en formato físico.\n2. Concentración de ingresos: El 18.4% del catálogo (Blockbusters) genera más de la mitad de las ganancias brutas totales.\n3. Tasa de falla en retail: El 24.3% del catálogo comercializado es un fracaso comercial y genera inventario muerto."
    )
    pdf.item_block(
        "Proponer al menos tres recomendaciones basadas en los resultados",
        "1. Cero discos físicos para indies: Comercializar los títulos del clúster digital exclusivamente por internet, ahorrando el 100% de costos de empaque y flete.\n2. Ediciones físicas enfocadas: Concentrar la producción de cajas plásticas únicamente en juegos de consola coleccionables.\n3. Remates tempranos: Aplicar descuentos agresivos el primer mes a juegos del clúster de fracasos para recuperar capital antes de que su valor colapse."
    )
    pdf.item_block(
        "Explicar las limitaciones del modelo desarrollado",
        "K-Means presupone grupos hiper-esféricos de varianza similar y no contempla estacionalidad temporal (ofertas de verano o Black Friday). Se recomienda complementar con algoritmos basados en densidad como DBSCAN."
    )

    output_path = "docs/Practica_Examen.pdf"
    os.makedirs("docs", exist_ok=True)
    pdf.output(output_path)
    print(f"PDF exclusivo de Práctica Examen (Partes 2, 3, 4 y 5) generado: {output_path}")

if __name__ == "__main__":
    build_practica_examen_pdf()
