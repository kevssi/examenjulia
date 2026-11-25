"""
Generador del Reporte Oficial Académico en PDF
Documentacion_Oficial_Proyecto_KMeans_Videojuegos.pdf
Cubre estrictamente los 8 apartados de la rúbrica institucional (Partes 1 a 8 completas).
Tipografía TrueType Arial 12, títulos en negrita, tablas completas de registros,
logo oficial de UTSLRC, sin encabezados de página, sin pies de página y sin leyendas de figura.
"""

import os
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class OfficialCleanDocPDF(FPDF):
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

    def section_title(self, num_str, title_str):
        self.ln(2)
        self.set_font("Arial", "B", 13)
        self.set_text_color(17, 24, 39)
        self.cell(0, 7, f"{num_str}. {title_str.upper()}", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(209, 213, 219)
        self.set_line_width(0.4)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(3)

    def paragraph(self, text, bold_prefix=None):
        if bold_prefix:
            self.set_font("Arial", "B", 12)
            self.set_text_color(17, 24, 39)
            self.write(5.8, f"{bold_prefix} ")
        self.set_font("Arial", "", 12)
        self.set_text_color(55, 65, 81)
        self.write(5.8, f"{text}\n\n")

    def bullet(self, title, desc):
        self.set_font("Arial", "B", 12)
        self.set_text_color(17, 24, 39)
        self.write(5.8, f"• {title}: ")
        self.set_font("Arial", "", 12)
        self.set_text_color(55, 65, 81)
        self.write(5.8, f"{desc}\n\n")

def build_clean_documentation_pdf():
    pdf = OfficialCleanDocPDF()

    raw_path = "data/videojuegos_ventas_original.csv"
    if not os.path.exists(raw_path):
        raw_path = "videojuegos_ventas_original.csv"
    df_raw = pd.read_csv(raw_path)

    # =========================================================================
    # 1. PORTADA OFICIAL
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
    pdf.cell(0, 9, "DOCUMENTACIÓN OFICIAL DEL PROYECTO", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 8, "Ventas del Formato Físico y Digital de los Videojuegos", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "mediante Algoritmo No Supervisado K-Means", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

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
    # 2. INTRODUCCIÓN Y PLANTEAMIENTO DEL PROBLEMA
    # =========================================================================
    pdf.add_page()
    pdf.section_title("2", "Introducción y Planteamiento del Problema")
    
    pdf.paragraph(
        "En la última década, la industria global de los videojuegos ha experimentado una transformación estructural definitiva: "
        "la migración paulatina del formato físico tradicional (discos y cartuchos comercializados en tiendas físicas) hacia los canales "
        "de descarga directa y servicios digitales (PlayStation Store, Xbox Network, Nintendo eShop y Steam). "
        "En la actualidad, ambos canales coexisten bajo patrones de consumo sumamente diferenciados.",
        bold_prefix="Contexto de la Industria:"
    )
    
    pdf.paragraph(
        "La problemática central que enfrentan las tiendas minoristas y distribuidoras radica en el riesgo de pérdidas económicas e "
        "inventario estancado en almacenes, provocado por la incertidumbre sobre qué títulos tienen alta demanda comercial, cuáles "
        "terminarán siendo fracasos y en qué formato específico (físico o digital) se desempeña mejor cada título. "
        "Mandar a fabricar decenas de miles de discos y empaques plásticos para un videojuego que nadie compra en tienda física genera "
        "costos de manufactura y bodegaje irrecuperables. Por otro lado, existen géneros (como shooters multijugador e indies) que venden "
        "millones exclusivamente por descarga digital; producir cajas físicas para ellos es un desperdicio financiero innecesario.",
        bold_prefix="Planteamiento de la Problemática:"
    )

    pdf.paragraph(
        "Con un volumen de lanzamientos cercano a los mil títulos anuales, resulta inviable clasificar manualmente el catálogo sin incurrir en sesgos. "
        "Por ello, este proyecto implementa Minería de Datos y Aprendizaje Automático No Supervisado con el algoritmo K-Means, permitiendo descubrir "
        "de manera autónoma los patrones naturales de rendimiento y clasificar los productos en perfiles comerciales concretos para la toma de decisiones.",
        bold_prefix="Justificación del Proyecto:"
    )

    # =========================================================================
    # 3. OBJETIVOS
    # =========================================================================
    pdf.section_title("3", "Objetivos del Proyecto")
    
    pdf.paragraph(
        "Desarrollar e implementar un modelo de segmentación multivariada no supervisada utilizando el algoritmo K-Means sobre un catálogo de 920 videojuegos, "
        "identificando perfiles arquetípicos de ventas físicas y digitales para optimizar la gestión de inventario y la estrategia comercial.",
        bold_prefix="Objetivo General:"
    )
    
    pdf.paragraph("Objetivos Específicos:")
    pdf.bullet("1. Auditoría y Preparación de Datos", "Limpiar y auditar el dataset resolviendo inconsistencias, registros duplicados, valores negativos y nulos mediante imputación contextual con la mediana por género, y normalizar las variables con StandardScaler.")
    pdf.bullet("2. Modelado y Evaluación de K", "Evaluar cuantitativamente al menos cinco configuraciones de K mediante el Método del Codo (Inercia / SSE) y el Coeficiente de Silueta, seleccionando y justificando K=4.")
    pdf.bullet("3. Reducción y Análisis Dimensional", "Aplicar Análisis de Componentes Principales (PCA en 2D) para visualizar e interpretar geométricamente los centroides y la cohesión interna de los clústeres descubiertos.")
    pdf.bullet("4. Despliegue en Dashboard Interactivo", "Construir una plataforma analítica en Streamlit con indicadores KPI en tiempo real, gráficas analíticas interactivas, dos páginas de navegación y filtros multivariados funcionales.")

    # =========================================================================
    # 4. OBTENCIÓN Y EXPLORACIÓN DEL DATASET (PARTE 2 DE LA RÚBRICA)
    # =========================================================================
    pdf.add_page()
    pdf.section_title("4", "Obtención y Exploración del Dataset")
    
    pdf.paragraph(
        "El dataset fue recopilado a partir de fuentes públicas consolidadas de la industria: VGChartz (registro de ventas físicas en retail), "
        "Metacritic (calificaciones promedio otorgadas por la prensa especializada) y Kaggle Video Game Sales Dataset. "
        "El archivo original cuenta con 928 filas y 12 columnas (superando ampliamente el requerimiento de 500 registros y 5 variables). "
        "Se importó en Python mediante la instrucción pd.read_csv('data/videojuegos_ventas_original.csv').",
        bold_prefix="Fuente, Dimensiones e Importación:"
    )

    pdf.paragraph(
        "Muestra de los primeros 10 registros del dataset original (df_raw.head(10)):",
        bold_prefix="Primeros 10 Registros:"
    )

    # Tabla visual de 10 registros originales
    cols_w = [18, 50, 24, 28, 18, 18, 18]
    headers = ["ID", "Título", "Género", "Plataforma", "V. Fís", "V. Dig", "Precio"]
    
    pdf.set_font("Arial", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    for i, h in enumerate(headers):
        nx = XPos.LMARGIN if i == len(headers) - 1 else XPos.RIGHT
        ny = YPos.NEXT if i == len(headers) - 1 else YPos.TOP
        pdf.cell(cols_w[i], 5.0, h, border=1, align="C", fill=True, new_x=nx, new_y=ny)

    pdf.set_font("Arial", "", 7.0)
    for _, r in df_raw.head(10).iterrows():
        pdf.cell(cols_w[0], 4.5, str(r["id_juego"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[1], 4.5, f" {str(r['titulo'])[:25]}", border=1, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[2], 4.5, str(r["genero"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[3], 4.5, str(r["plataforma"])[:14], border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[4], 4.5, f"{r['ventas_fisicas_millones']:.2f}M", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[5], 4.5, f"{r['ventas_digitales_millones']:.2f}M" if pd.notnull(r['ventas_digitales_millones']) else "Nulo", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[6], 4.5, f"${r['precio_lanzamiento_usd']:.2f}" if pd.notnull(r['precio_lanzamiento_usd']) else "Nulo", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(4)

    pdf.paragraph(
        "El dataset contiene 5 columnas categóricas de texto (id_juego, titulo, genero, plataforma, distribuidora) y 7 numéricas "
        "(anio_lanzamiento, ventas_fisicas_millones, ventas_digitales_millones, ventas_totales_millones, precio_lanzamiento_usd, "
        "calificacion_critica y horas_juego). Mediante df.describe() se identificaron promedios de 3.42M en ventas físicas, 5.76M en digitales, "
        "precio medio de $52.42 USD, calificación de 76.35 pts y duración de 31.48 horas, revelando además inconsistencias con valores negativos "
        "(-2.50M en ventas y -$59.99 USD en precio).",
        bold_prefix="Columnas, Tipos y Estadísticas Descriptivas:"
    )

    pdf.paragraph(
        "Se auditaron los datos identificando 8 registros duplicados exactos y 17 valores nulos (5 en ventas digitales, 6 en precio y 6 en calificación). "
        "Para la exploración visual se crearon 4 gráficas: matriz de correlación (Heatmap), dispersión de ventas, boxplot de distribución y gráfico de dona. "
        "Se seleccionaron 5 variables continuas clave para el modelo (ventas físicas y digitales para capturar los canales, precio para medir la barrera económica, "
        "calificación para medir aceptación crítica y horas de juego para medir volumen de contenido).",
        bold_prefix="Nulos, Duplicados, Gráficas y Selección de Variables:"
    )

    # Gráfica de correlación
    img_hm = "assets/1_heatmap_correlacion.png"
    if os.path.exists(img_hm):
        pdf.image(img_hm, x=55, y=pdf.get_y(), w=100)
        pdf.ln(78)

    # =========================================================================
    # 5. LIMPIEZA, PREPARACIÓN Y K-MEANS (PARTES 3 Y 4 DE LA RÚBRICA)
    # =========================================================================
    pdf.add_page()
    pdf.section_title("5", "Limpieza, Preparación y Modelado K-Means")

    pdf.paragraph(
        "Se aplicó un riguroso protocolo de limpieza y preparación de datos para garantizar la validez del agrupamiento:",
        bold_prefix="Limpieza y Preparación de Datos (Parte 3):"
    )
    pdf.bullet("1. Eliminación de Duplicados", "Se eliminaron los 8 registros duplicados exactos mediante drop_duplicates(), reduciendo el catálogo a 920 registros limpios y únicos.")
    pdf.bullet("2. Corrección de Inconsistencias (Negativos)", "Se convirtieron los valores negativos accidentales a positivos aplicando valor absoluto con np.abs() a todas las variables numéricas.")
    pdf.bullet("3. Tratamiento de Valores Nulos", "Los 17 valores faltantes se imputaron contextualmente con la mediana calculada según el género del juego con fillna(groupby('genero')), evitando distorsiones de la media global.")
    pdf.bullet("4. Tratamiento de Valores Atípicos (Outliers)", "Se detectaron outliers legítimos con ventas superiores a 15-20M de copias (Superventas Blockbusters). Se justificó NO eliminarlos porque son fenómenos comerciales reales e indispensables para el negocio; su magnitud se equilibró mediante el escalamiento.")
    pdf.bullet("5. Escalamiento con StandardScaler", "Se aplicó StandardScaler() sobre las 5 variables numéricas continuas para normalizarlas a Media = 0 y Varianza = 1. Esta transformación es indispensable para que el precio ($20-$70) o la calificación (0-100) no dominen sobre los millones de copias (0-15M) en la distancia euclidiana.")

    # Gráfica del codo y silueta
    img_k = "assets/2_codo_silueta.png"
    if os.path.exists(img_k):
        pdf.image(img_k, x=25, y=pdf.get_y(), w=160)
        pdf.ln(68)

    pdf.paragraph(
        "Se evaluaron 7 valores de K (K=2 a K=8) con Scikit-Learn. Se seleccionó K=4 como la configuración definitiva. "
        "En K=4 se ubica el punto de mayor inflexión del Método del Codo (Inercia = 1,415.33) y se alcanza el máximo global del Coeficiente de Silueta (0.4197). "
        "Al comparar con K=3 (Inercia = 1,885.41, Silueta = 0.4141), K=3 fusionaba en un solo grupo mixto a los indies digitales con los juegos de consola tradicional, "
        "perdiendo la capacidad de distinguir los canales de venta. K=4 separa con total nitidez ambos modelos comerciales.",
        bold_prefix="Evaluación de K, Justificación y Comparación de Modelos (Parte 4):"
    )

    # =========================================================================
    # 6. ANÁLISIS E INTERPRETACIÓN DE RESULTADOS (PARTE 5 DE LA RÚBRICA)
    # =========================================================================
    pdf.add_page()
    pdf.section_title("6", "Análisis e Interpretación de Resultados")

    pdf.paragraph(
        "A continuación se presenta la tabla comparativa consolidada con los centroides desescalados a unidades reales y la cantidad de registros por grupo:",
        bold_prefix="Tabla Comparativa de los Grupos y Centroides:"
    )

    # Tabla de Centroides formal
    pdf.set_font("Arial", "B", 8.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.set_text_color(17, 24, 39)
    pdf.set_draw_color(209, 213, 219)
    
    cols_c = [60, 22, 22, 22, 22, 24]
    pdf.cell(cols_c[0], 6, "Clúster Asignado", border=1, align="C", fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(cols_c[1], 6, "V. Física", border=1, align="C", fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(cols_c[2], 6, "V. Digital", border=1, align="C", fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(cols_c[3], 6, "Precio Medio", border=1, align="C", fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(cols_c[4], 6, "Calif. Media", border=1, align="C", fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(cols_c[5], 6, "Cantidad (%)", border=1, align="C", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    centroides = [
        ("Superventas Globales (Blockbusters)", "8.69 M", "12.39 M", "$69.99 USD", "87.7 pts", "169 (18.4%)"),
        ("Fracasos Comerciales y Bajo Rendimiento", "0.41 M", "0.57 M", "$55.97 USD", "52.7 pts", "224 (24.3%)"),
        ("Coleccionables de Consola (Físico Fuerte)", "6.65 M", "2.87 M", "$61.28 USD", "84.1 pts", "210 (22.8%)"),
        ("Éxitos Digitales e Indies Virales", "0.60 M", "7.71 M", "$35.01 USD", "81.7 pts", "317 (34.5%)")
    ]

    pdf.set_font("Arial", "", 8)
    pdf.set_text_color(55, 65, 81)
    for c_n, c_f, c_d, c_p, c_ca, c_v in centroides:
        pdf.cell(cols_c[0], 5.5, f" {c_n}", border=1, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_c[1], 5.5, c_f, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_c[2], 5.5, c_d, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_c[3], 5.5, c_p, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_c[4], 5.5, c_ca, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_c[5], 5.5, f" {c_v}", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(4)

    # Gráficas de soporte en paralelo
    img_pca = "assets/3_pca_clusters.png"
    img_box = "assets/4_boxplot_ventas.png"
    y_g = pdf.get_y()
    if os.path.exists(img_pca) and os.path.exists(img_box):
        pdf.image(img_pca, x=20, y=y_g, w=82)
        pdf.image(img_box, x=108, y=y_g, w=82)
        pdf.ln(58)

    pdf.paragraph(
        "Se proyectó el modelo en 2D mediante PCA reteniendo el 75.2% de la varianza total (49.9% en PC1 y 25.4% en PC2). "
        "PC1 refleja el éxito comercial global, mientras que PC2 captura la polarización entre ventas físicas y digitales. "
        "Los Éxitos Digitales (34.5%) venden 13 veces más por descarga que en disco a precio accesible ($35 USD). "
        "Los Coleccionables de Consola (22.8%) dominan el canal físico en Switch y PlayStation ($61 USD). "
        "Los Blockbusters (18.4%) lideran ambos canales a precio completo ($70 USD), y los Fracasos (24.3%) presentan ventas nulas en ambos formatos.",
        bold_prefix="Características y Diferencias entre Grupos:"
    )

    # =========================================================================
    # 7. DASHBOARD INTERACTIVO (STREAMLIT)
    # =========================================================================
    pdf.add_page()
    pdf.section_title("7", "Dashboard Interactivo (Streamlit)")
    
    pdf.paragraph(
        "Se diseñó una aplicación analítica en Streamlit con diseño formal sobrio, sin elementos distractores e integrando 5 filtros dinámicos con lógica AND:",
        bold_prefix="Estructura de la Plataforma:"
    )
    pdf.bullet("Página 1: Análisis General", "Presenta cuatro tarjetas KPI en tiempo real (Total juegos, Venta digital media, Venta física media y Puntaje de crítica), gráfica de dispersión de canales, comparativa de ventas físicas vs. digitales por género en barras agrupadas, volumen por plataforma y matriz de correlación.")
    pdf.bullet("Página 2: Segmentación K-Means", "Exhibe la distribución porcentual en gráfico de dona (18.4% Blockbusters, 34.5% Éxitos Digitales, 22.8% Coleccionables y 24.3% Fracasos), proyección en PCA 2D, boxplot de ventas totales por clúster, relación de ventas vs. calificación y tabla de auditoría con buscador.")
    pdf.bullet("Barra Lateral de Filtros", "Permite alternar entre ambas páginas y filtrar simultáneamente por Clúster, Género, Plataforma, Slider de Precio (USD) y Slider de Calificación de la crítica.")

    # Imagen de dona
    img_dona = "assets/5_dona_proporcion.png"
    if os.path.exists(img_dona):
        pdf.image(img_dona, x=65, y=pdf.get_y(), w=80)
        pdf.ln(68)

    # =========================================================================
    # 8. CONCLUSIONES, RECOMENDACIONES Y LIMITACIONES
    # =========================================================================
    pdf.add_page()
    pdf.section_title("8", "Conclusiones, Recomendaciones y Limitaciones")

    pdf.paragraph("Tres Hallazgos Principales (Parte 5):")
    pdf.bullet("1. Predominancia del Canal Digital", "El 34.5% de los videojuegos (Éxitos Digitales) vende 13 veces más por descarga digital que en formato físico (7.71 M vs. 0.60 M). Producir discos físicos para estos juegos representa una pérdida financiera directa.")
    pdf.bullet("2. Concentración de Rentabilidad", "Menos del 20% del catálogo (Superventas Blockbusters) genera más de la mitad de los ingresos comerciales brutos globales en ambos canales.")
    pdf.bullet("3. Tasa de Falla en Tiendas", "El 24.3% de los títulos lanzados es un fracaso comercial con ventas inferiores a 0.6M y calificaciones reprobatorias (52.7 puntos), siendo la causa principal de inventario muerto.")

    pdf.paragraph("Tres Recomendaciones Estratégicas Basadas en Resultados (Parte 5):")
    pdf.bullet("1. Política Cero Discos Físicos para Indies", "Comercializar los juegos del Clúster de Éxitos Digitales exclusivamente por internet, ahorrando el 100% de los costos de manufactura plástica y logística.")
    pdf.bullet("2. Producción Focalizada en Coleccionables", "Concentrar la impresión de cajas y cartuchos únicamente en juegos de consola tradicional (Switch / PlayStation) donde los usuarios exigen el formato físico.")
    pdf.bullet("3. Liquidación Rápida de Fracasos Comerciales", "Aplicar descuentos agresivos del 50% al 70% durante las primeras semanas para los títulos del Clúster de Fracasos, recuperando liquidez antes de que su valor comercial decaiga totalmente.")

    pdf.paragraph(
        "K-Means presupone grupos hiper-esféricos de varianza similar y no contempla variaciones temporales estacionales (como ofertas de fin de año o Black Friday). "
        "Asimismo, no modela relaciones de causalidad directa. Como trabajo futuro, se recomienda integrar modelos de series de tiempo y algoritmos basados en densidad como DBSCAN.",
        bold_prefix="Limitaciones del Modelo Desarrollado (Parte 5):"
    )

    output_path = "docs/Documentacion_Oficial_Proyecto_KMeans_Videojuegos.pdf"
    os.makedirs("docs", exist_ok=True)
    pdf.output(output_path)
    print(f"Documento oficial actualizado exitosamente: {output_path}")

if __name__ == "__main__":
    build_clean_documentation_pdf()
