"""
Generador del PDF oficial Practica_Examen.pdf
Integra TODAS las respuestas escritas punto por punto de las Partes 2, 3, 4 y 5
junto con las tablas de registros y salidas numéricas de respaldo.
Tipografía Arial 12, títulos en negrita y logo oficial UTSLRC en la portada.
"""

import os
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class PracticaExamenDocPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=18, top=16, right=18)
        self.add_font("Arial", "", "C:/Windows/Fonts/arial.ttf")
        self.add_font("Arial", "B", "C:/Windows/Fonts/arialbd.ttf")

    def header(self):
        pass

    def footer(self):
        pass

    def part_title(self, num_str, title_str):
        self.ln(3)
        self.set_font("Arial", "B", 13)
        self.set_text_color(17, 24, 39)
        self.cell(0, 7, f"PARTE {num_str}. {title_str.upper()}", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(209, 213, 219)
        self.set_line_width(0.4)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(3)

    def item_block(self, item_title, content_text):
        self.set_font("Arial", "B", 12)
        self.set_text_color(17, 24, 39)
        self.write(5.8, f"- {item_title}:\n")
        self.set_font("Arial", "", 12)
        self.set_text_color(55, 65, 81)
        self.write(5.8, f"  Respuesta: {content_text}\n\n")

def build_pdf():
    in_path = "data/videojuegos_ventas_original.csv"
    proc_path = "data/videojuegos_ventas_procesado.csv"
    df_raw = pd.read_csv(in_path)
    df_proc = pd.read_csv(proc_path)

    pdf = PracticaExamenDocPDF()

    # =========================================================================
    # PORTADA
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
        "El dataset seleccionado cuenta con 928 filas y 12 variables (cumple y supera ampliamente el mínimo requerido de 500 registros y 5 variables)."
    )
    pdf.item_block(
        "Identificar la fuente de obtención de los datos",
        "Registros consolidados de ventas de la industria a nivel global: VGChartz (registro de ventas físicas en retail), Metacritic (calificaciones promedio otorgadas por la prensa especializada) y Kaggle Video Game Sales Dataset."
    )
    pdf.item_block(
        "Importar el dataset en Python utilizando read_csv() o read_excel()",
        "Implementado con la librería Pandas mediante: df_raw = pd.read_csv('data/videojuegos_ventas_original.csv')."
    )
    pdf.item_block(
        "Mostrar los primeros 10 registros",
        "Ejecutado con df_raw.head(10). A continuación se presenta la tabla visual con los primeros 10 registros del dataset original:"
    )

    # Tabla visual de 10 registros originales
    cols_w = [18, 50, 24, 28, 18, 18, 18]
    headers = ["ID", "Título", "Género", "Plataforma", "V. Fís", "V. Dig", "Precio"]
    
    pdf.set_font("Arial", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    for i, h in enumerate(headers):
        nx = XPos.LMARGIN if i == len(headers) - 1 else XPos.RIGHT
        ny = YPos.NEXT if i == len(headers) - 1 else YPos.TOP
        pdf.cell(cols_w[i], 5.2, h, border=1, align="C", fill=True, new_x=nx, new_y=ny)

    pdf.set_font("Arial", "", 7.0)
    for _, r in df_raw.head(10).iterrows():
        pdf.cell(cols_w[0], 4.8, str(r["id_juego"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[1], 4.8, f" {str(r['titulo'])[:25]}", border=1, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[2], 4.8, str(r["genero"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[3], 4.8, str(r["plataforma"])[:14], border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[4], 4.8, f"{r['ventas_fisicas_millones']:.2f}M", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[5], 4.8, f"{r['ventas_digitales_millones']:.2f}M" if pd.notnull(r['ventas_digitales_millones']) else "Nulo", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[6], 4.8, f"${r['precio_lanzamiento_usd']:.2f}" if pd.notnull(r['precio_lanzamiento_usd']) else "Nulo", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)

    pdf.item_block(
        "Identificar las dimensiones, columnas y tipos de datos",
        "Dimensiones: 928 filas x 12 columnas. Columnas de texto (object): id_juego, titulo, genero, plataforma, distribuidora. Columnas numéricas (float64/int64): anio_lanzamiento, ventas_fisicas_millones, ventas_digitales_millones, ventas_totales_millones, precio_lanzamiento_usd, calificacion_critica y horas_juego."
    )
    pdf.item_block(
        "Obtener estadísticas descriptivas",
        "Calculadas mediante df_raw.describe(): Venta física media = 3.42 M, Venta digital media = 5.76 M, Precio medio = $52.42 USD, Calificación crítica media = 76.35 puntos y Horas de juego promedio = 31.48 horas. Los mínimos revelaron inconsistencias negativas (-2.50 M en ventas y -$59.99 en precio)."
    )
    pdf.item_block(
        "Identificar valores nulos y registros duplicados",
        "Se detectaron 8 registros duplicados exactos mediante df_raw.duplicated().sum(). Asimismo, se detectaron 17 valores nulos con df_raw.isnull().sum() (5 en ventas digitales, 6 en precio de lanzamiento y 6 en calificación de la crítica)."
    )
    pdf.item_block(
        "Crear al menos tres gráficas exploratorias",
        "Se elaboraron 4 visualizaciones: 1) Matriz de correlación Heatmap, 2) Gráfico de dispersión de ventas físicas vs. digitales, 3) Diagrama de cajas Boxplot de ventas por clúster, y 4) Gráfica de dona de proporciones del catálogo."
    )
    pdf.item_block(
        "Seleccionar al menos tres variables relevantes para el agrupamiento y justificar su elección",
        "Se seleccionaron 5 variables continuas clave: ventas_fisicas_millones y ventas_digitales_millones (definen los dos canales de distribución del mercado), precio_lanzamiento_usd (evalúa la barrera de costo comercial), calificacion_critica (mide la recepción y tracción del mercado) y horas_juego (mide la duración y cantidad de contenido)."
    )

    # =========================================================================
    # PARTE 3. LIMPIEZA Y PREPARACIÓN DE DATOS
    # =========================================================================
    pdf.add_page()
    pdf.part_title("3", "Limpieza y preparación de datos")

    pdf.item_block(
        "Identificar y corregir inconsistencias en los datos",
        "Se identificaron valores negativos anómalos en precio y ventas físicas originados por errores de captura. Se corrigieron aplicando la función de valor absoluto np.abs() a todas las variables numéricas."
    )
    pdf.item_block(
        "Realizar el tratamiento de valores nulos y registros duplicados",
        "Se eliminaron los 8 registros duplicados exactos con drop_duplicates(), reduciendo el catálogo a 920 registros limpios. Los 17 valores nulos se trataron mediante imputación contextual con la mediana agrupada por género del videojuego, evitando el sesgo que causaría la media global."
    )
    pdf.item_block(
        "Verificar y corregir los tipos de datos cuando sea necesario",
        "Se forzó el casteo correcto a float64 en variables continuas (ventas y precio) y a int64 en calificación y horas de juego."
    )
    pdf.item_block(
        "Identificar valores atípicos y justificar su tratamiento",
        "Se identificaron outliers legítimos con ventas superiores a 20M de copias (Superventas Blockbusters). Se justificó NO eliminarlos porque representan los casos comerciales de mayor éxito de la industria, indispensables para la segmentación."
    )
    pdf.item_block(
        "Aplicar transformaciones o codificaciones cuando sea necesario",
        "Se calculó la variable acumulada 'ventas_totales_millones' (físicas + digitales), se corrigieron inconsistencias de signo con np.abs(), y para el agrupamiento se preservaron las 5 variables continuas cuantitativas para garantizar el cálculo métrico euclidiano directo sin inducir distorsiones de dimensionalidad."
    )
    pdf.item_block(
        "Implementar una técnica de escalamiento, como StandardScaler",
        "Se implementó StandardScaler() de Scikit-Learn sobre las 5 variables numéricas continuas, normalizando cada una a Media = 0 y Varianza = 1."
    )
    pdf.item_block(
        "Mostrar los resultados de la limpieza y preparación de datos",
        "El dataset pasó de 928 filas con anomalías a 920 filas limpias, guardadas en data/videojuegos_ventas_procesado.csv, con 0 valores nulos y 0 valores negativos restantes. A continuación se muestran los primeros 10 registros limpios y preparados:"
    )

    # Tabla visual de 10 registros limpios
    pdf.set_font("Arial", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    for i, h in enumerate(headers):
        nx = XPos.LMARGIN if i == len(headers) - 1 else XPos.RIGHT
        ny = YPos.NEXT if i == len(headers) - 1 else YPos.TOP
        pdf.cell(cols_w[i], 5.2, h, border=1, align="C", fill=True, new_x=nx, new_y=ny)

    pdf.set_font("Arial", "", 7.0)
    for _, r in df_proc.head(10).iterrows():
        pdf.cell(cols_w[0], 4.8, str(r["id_juego"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[1], 4.8, f" {str(r['titulo'])[:25]}", border=1, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[2], 4.8, str(r["genero"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[3], 4.8, str(r["plataforma"])[:14], border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[4], 4.8, f"{r['ventas_fisicas_millones']:.2f}M", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[5], 4.8, f"{r['ventas_digitales_millones']:.2f}M", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[6], 4.8, f"${r['precio_lanzamiento_usd']:.2f}", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)

    pdf.item_block(
        "Explicar la importancia de las transformaciones realizadas",
        "K-Means calcula distancias euclidianas en el espacio multidimensional. Sin StandardScaler, la calificación (0 a 100) y el precio ($20 a $80) habrían tenido un peso numérico 50 veces superior al de las ventas (0 a 15 M), anulando por completo la influencia de los canales de venta en los clústeres."
    )

    # =========================================================================
    # PARTE 4. IMPLEMENTACIÓN DEL ALGORITMO K-MEANS
    # =========================================================================
    pdf.add_page()
    pdf.part_title("4", "Implementación del algoritmo K-Means")

    pdf.item_block(
        "Seleccionar al menos tres variables para el entrenamiento del modelo",
        "Se seleccionaron 5 variables continuas normalizadas: ventas_fisicas_millones, ventas_digitales_millones, precio_lanzamiento_usd, calificacion_critica y horas_juego."
    )
    pdf.item_block(
        "Implementar el algoritmo K-Means utilizando Scikit-learn",
        "Implementado con Scikit-learn mediante: from sklearn.cluster import KMeans; kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)."
    )
    pdf.item_block(
        "Evaluar al menos cinco valores diferentes de K",
        "Se evaluaron 7 valores diferentes de K (K=2 hasta K=8) calculando la Inercia (SSE) y el Coeficiente de Silueta. A continuación se presentan los resultados numéricos de la evaluación:"
    )

    # Tabla de evaluación de K
    k_eval_data = [
        ("K=2", "2,947.74", "0.3373"),
        ("K=3", "1,885.41", "0.4141"),
        ("K=4 (Óptimo Seleccionado)", "1,415.33", "0.4197"),
        ("K=5", "1,182.57", "0.3911"),
        ("K=6", "1,082.53", "0.3738"),
        ("K=7", "1,012.10", "0.3351"),
        ("K=8", "933.08", "0.2855"),
    ]
    kw = [55, 55, 55]
    pdf.set_font("Arial", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(kw[0], 5, "Configuración", border=1, align="C", fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(kw[1], 5, "Inercia (SSE)", border=1, align="C", fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(kw[2], 5, "Silhouette Score", border=1, align="C", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Arial", "", 7.5)
    for kv, inercia, sil in k_eval_data:
        pdf.set_font("Arial", "B" if "Óptimo" in kv else "", 7.5)
        pdf.cell(kw[0], 4.8, kv, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(kw[1], 4.8, inercia, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(kw[2], 4.8, sil, border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)

    pdf.item_block(
        "Seleccionar y justificar el número de clústeres más adecuado",
        "Se seleccionó K=4 como la solución óptima. Justificación: En K=4 se ubica el punto de inflexión del codo (Inercia = 1,415.33) y se alcanza el valor máximo del Coeficiente de Silueta (0.4197), con Calinski-Harabasz de 687.04 y Davies-Bouldin de 0.9637, separando con nitidez ambos canales de venta."
    )
    pdf.item_block(
        "Entrenar el modelo final utilizando KMeans",
        "Modelo final ajustado mediante: kmeans.fit(X_scaled) configurado con n_clusters=4."
    )
    pdf.item_block(
        "Asignar un clúster a cada registro mediante fit_predict()",
        "Clústeres asignados exitosamente a cada uno de los 920 registros mediante: df['Cluster'] = kmeans.fit_predict(X_scaled)."
    )
    pdf.item_block(
        "Obtener e interpretar los centroides",
        "Centroides obtenidos en unidades originales de negocio (valores medios reales por clúster). Revelan que los títulos independientes y digitales no requieren presencia física en anaqueles para triunfar, mientras que las franquicias de consola aún requieren soporte físico para coleccionistas:"
    )

    # Tabla de Centroides
    cw = [60, 22, 22, 22, 21, 27]
    cheaders = ["Clúster Asignado", "Vta Física", "Vta Digital", "Precio", "Calif.", "Proporción"]

    pdf.set_font("Arial", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    for i, h in enumerate(cheaders):
        nx = XPos.LMARGIN if i == len(cheaders) - 1 else XPos.RIGHT
        ny = YPos.NEXT if i == len(cheaders) - 1 else YPos.TOP
        pdf.cell(cw[i], 5.5, h, border=1, align="C", fill=True, new_x=nx, new_y=ny)

    cdata = [
        ("Superventas Globales (Blockbusters)", "8.69 M", "12.39 M", "$69.87", "87.7 pts", "169 (18.4%)"),
        ("Fracasos Comerciales y Bajo Rendimiento", "0.41 M", "0.57 M", "$55.97", "52.7 pts", "224 (24.3%)"),
        ("Coleccionables de Consola (Físico Fuerte)", "6.65 M", "2.87 M", "$61.28", "84.1 pts", "210 (22.8%)"),
        ("Éxitos Digitales e Indies Virales", "0.60 M", "7.71 M", "$35.01", "81.7 pts", "317 (34.5%)")
    ]

    pdf.set_font("Arial", "", 7.2)
    for c_nom, vf, vd, pr, ca, cnt in cdata:
        pdf.cell(cw[0], 5, f"  {c_nom}", border=1, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cw[1], 5, vf, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cw[2], 5, vd, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cw[3], 5, pr, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cw[4], 5, ca, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cw[5], 5, cnt, border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)

    pdf.item_block(
        "Identificar la cantidad de registros pertenecientes a cada clúster",
        "Distribución final de registros: Clúster de Éxitos Digitales con 317 juegos (34.5%), Clúster de Fracasos Comerciales con 224 juegos (24.3%), Clúster de Coleccionables de Consola con 210 juegos (22.8%) y Clúster de Superventas Blockbusters con 169 juegos (18.4%)."
    )
    pdf.item_block(
        "Crear al menos una gráfica para visualizar los agrupamientos",
        "Se implementó reducción de dimensionalidad mediante Análisis de Componentes Principales (PCA en 2D), proyectando los clústeres en 2 ejes ortogonales que explican el 75.2% de la varianza total (49.9% en PC1 y 25.4% en PC2)."
    )
    pdf.item_block(
        "Comparar dos configuraciones del modelo y explicar las diferencias encontradas",
        "Comparativa K=4 vs K=3: En K=3 (Inercia = 1,885.41, Silueta = 0.4141), el modelo fusiona erróneamente los juegos digitales y los títulos de consola en un único grupo mixto, perdiendo resolución estratégica. K=4 reduce la inercia un 25% y separa con nitidez absoluta los éxitos digitales de los coleccionables físicos."
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
        "Calculadas mediante df.groupby('Cluster_Nombre').mean() para todas las variables cuantitativas de ventas, precio, notas y duración."
    )
    pdf.item_block(
        "Interpretar los centroides obtenidos",
        "Los centroides demuestran que los videojuegos del segmento digital e indie no requieren prensado de discos para ser altamente rentables, mientras que los juegos de aventura y plataformas de consola requieren soporte físico para satisfacer a coleccionistas."
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
        "Tabla comparativa consolidada:\n- Blockbusters: 8.69M fís | 12.39M dig | $69.87 USD | 87.7 pts | 169 títulos (18.4%)\n- Fracasos Comerciales: 0.41M fís | 0.57M dig | $55.97 USD | 52.7 pts | 224 títulos (24.3%)\n- Coleccionables Consola: 6.65M fís | 2.87M dig | $61.28 USD | 84.1 pts | 210 títulos (22.8%)\n- Éxitos Digitales: 0.60M fís | 7.71M dig | $35.01 USD | 81.7 pts | 317 títulos (34.5%)"
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
    print(f"Documento Practica_Examen.pdf con respuestas escritas y tablas generado: {output_path}")

if __name__ == "__main__":
    build_pdf()
