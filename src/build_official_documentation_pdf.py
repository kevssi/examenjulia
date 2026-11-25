"""
Script para generar el Documento Oficial del Proyecto en formato académico limpio y sobrio:
docs/Documentacion_Oficial_Proyecto_KMeans_Videojuegos.pdf
SIN encabezados, SIN números de página ni pies, SIN leyendas de figura ('Figura X...'), SIN solapamientos de texto.
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class CleanDocumentPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=20, top=18, right=20)

    # 1. SIN ENCABEZADO
    def header(self):
        pass

    # 2. SIN PIE DE PÁGINA NI NÚMERO DE PÁGINA
    def footer(self):
        pass

    def section_title(self, num_str, title_str):
        self.ln(5)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(17, 24, 39) # Negro
        self.cell(0, 6, f"{num_str}. {title_str}", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(229, 231, 235)
        self.set_line_width(0.3)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(4)

    def paragraph(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(55, 65, 81)
        if bold_prefix:
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(17, 24, 39)
            self.write(4.8, bold_prefix + " ")
            self.set_font("Helvetica", "", 9)
            self.set_text_color(55, 65, 81)
        self.write(4.8, text + "\n\n")

    def bullet(self, title, desc):
        # Flujo continuo natural para evitar CUALQUIER solapamiento horizontal
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(17, 24, 39)
        self.write(4.8, f"- {title}: ")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(55, 65, 81)
        self.write(4.8, desc + "\n\n")


def build_clean_documentation_pdf():
    pdf = CleanDocumentPDF()
    pdf.alias_nb_pages()

    # =========================================================================
    # 1. PORTADA LIMPIA Y FORMAL (Sin encabezado ni pie)
    # =========================================================================
    pdf.add_page()
    pdf.ln(30)

    # Título principal
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(0, 8, "PROYECTO INTEGRADOR", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 7, "Segmentación de Rendimiento de Videojuegos Físicos vs. Digitales", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 6, "mediante Algoritmo No Supervisado K-Means", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(8)
    pdf.set_draw_color(209, 213, 219)
    pdf.set_line_width(0.5)
    pdf.line(50, pdf.get_y(), 160, pdf.get_y())

    pdf.ln(45)

    # Datos solicitados exactamente por el alumno
    campos = [
        ("Materia", "Extracción de Conocimiento en Bases de Datos"),
        ("Alumno", "Kevin Uriel Silva Talamantes"),
        ("Maestra", "Julia García"),
        ("Grupo", "TI3-9"),
        ("Fecha", "Noviembre de 2026")
    ]

    for etiqueta, valor in campos:
        pdf.set_x(45)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(31, 41, 55)
        pdf.cell(30, 7, f"{etiqueta}:", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(55, 65, 81)
        pdf.cell(0, 7, valor, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
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
    # 4. DESCRIPCIÓN DEL DATASET
    # =========================================================================
    pdf.add_page()
    pdf.section_title("4", "Descripción del Dataset")
    
    pdf.paragraph(
        "El dataset fue recopilado a partir de fuentes públicas y registros consolidados de la industria (VGChartz / Metacritic / Kaggle Video Game Sales Dataset). "
        "El archivo original cuenta con 928 filas y 12 columnas, conteniendo tanto atributos descriptivos como métricas cuantitativas de ventas y mercado.",
        bold_prefix="Origen y Características:"
    )

    # Tabla limpia de variables
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(243, 244, 246)
    pdf.set_text_color(17, 24, 39)
    pdf.set_draw_color(209, 213, 219)
    
    cols = [38, 22, 24, 86]
    pdf.cell(cols[0], 6, "Variable", 1, 0, "C", True)
    pdf.cell(cols[1], 6, "Tipo", 1, 0, "C", True)
    pdf.cell(cols[2], 6, "Escala / Rango", 1, 0, "C", True)
    pdf.cell(cols[3], 6, "Descripción", 1, 1, "C", True)

    vars_info = [
        ("id_juego", "Texto", "GAME-0001...", "Identificador único asignado a cada videojuego."),
        ("titulo", "Texto", "Nombre comercial", "Título del videojuego y edición de lanzamiento."),
        ("genero", "Texto", "9 géneros", "Acción, Aventura, Deportes, RPG, Shooter, Indie, etc."),
        ("plataforma", "Texto", "6 plataformas", "PS5, PS4, Xbox Series, Xbox One, Switch y PC."),
        ("ventas_fisicas_millones", "Numérico", "0.01 a 15.0 M", "Copias en cartucho/disco físico vendidas a nivel global."),
        ("ventas_digitales_millones", "Numérico", "0.02 a 20.0 M", "Copias descargadas por canales digitales a nivel global."),
        ("ventas_totales_millones", "Numérico", "0.03 a 35.0 M", "Suma acumulada del volumen de ventas de ambos canales."),
        ("precio_lanzamiento_usd", "Numérico", "$19.99 a $79.99", "Precio oficial de venta sugerido al público en USD."),
        ("calificacion_critica", "Numérico", "30 a 98 puntos", "Puntaje de aceptación otorgado por la prensa especializada."),
        ("horas_juego", "Numérico", "5 a 120 horas", "Duración media estimada de la campaña principal.")
    ]

    pdf.set_font("Helvetica", "", 7.8)
    pdf.set_text_color(55, 65, 81)
    for v_nom, v_tipo, v_rng, v_desc in vars_info:
        pdf.cell(cols[0], 5.2, f" {v_nom}", 1, 0, "L")
        pdf.cell(cols[1], 5.2, v_tipo, 1, 0, "C")
        pdf.cell(cols[2], 5.2, v_rng, 1, 0, "C")
        pdf.cell(cols[3], 5.2, f" {v_desc}", 1, 1, "L")

    pdf.ln(5)

    # Gráfica centrada de correlación (SIN TEXTO DE LEYENDA 'Figura 1...')
    img_hm = "assets/reporte_videojuegos/1_heatmap_correlacion.png"
    if os.path.exists(img_hm):
        pdf.image(img_hm, x=55, y=pdf.get_y(), w=100)
        pdf.ln(82)

    # =========================================================================
    # 5. DESARROLLO DEL PROYECTO
    # =========================================================================
    pdf.add_page()
    pdf.section_title("5", "Desarrollo del Proyecto: Limpieza, Preparación y K-Means")

    pdf.paragraph(
        "El preprocesamiento de datos se desarrolló bajo tres etapas indispensables para asegurar la calidad de los agrupamientos:",
        bold_prefix="Auditoría y Limpieza:"
    )
    pdf.bullet("1. Eliminación de Duplicados", "Se identificaron 8 filas duplicadas exactas generadas durante la consolidación de fuentes, procediendo a su eliminación para no distorsionar las densidades de puntos (dejando 920 registros limpios).")
    pdf.bullet("2. Corrección de Valores Negativos", "Se corrigieron valores anómalos negativos en precio y ventas físicas originados por errores de digitación, aplicando la función de valor absoluto np.abs().")
    pdf.bullet("3. Imputación Contextual de Nulos", "Se trataron 17 valores nulos (5 en ventas digitales, 6 en precio y 6 en calificación). Se aplicó imputación por mediana condicional según el género de cada juego, evitando la distorsión que ocasionaría la media aritmética global ante títulos extremos.")
    pdf.bullet("4. Estandarización con StandardScaler", "Debido a que las ventas están medidas en millones (0 a 15), el precio en decenas de dólares ($20 a $80) y la calificación en escala de 0 a 100, se aplicó StandardScaler para normalizar las 5 variables a media 0 y varianza 1. Sin esta transformación, la calificación y el precio habrían dominado el 90% del cálculo de distancias euclidianas.")

    # Gráfica del codo y silueta (SIN TEXTO 'Figura 2...')
    img_k = "assets/reporte_videojuegos/2_codo_silueta.png"
    if os.path.exists(img_k):
        pdf.image(img_k, x=25, y=pdf.get_y(), w=160)
        pdf.ln(70)

    pdf.paragraph(
        "Se evaluaron 7 valores de K (desde K=2 hasta K=8). Se seleccionó K=4 como la configuración óptima. "
        "En K=4 se ubica el punto de inflexión del codo (Inercia = 1,415.33) y se obtiene el valor máximo de Silueta (0.4197), con Calinski-Harabasz de 687.04 y Davies-Bouldin de 0.9637. "
        "En comparación con K=3 (Inercia = 1,885.4, Silueta = 0.4141), K=3 fusionaba erróneamente los títulos digitales con los de consola en un único grupo mixto, perdiendo resolución comercial. K=4 separa con total nitidez ambos canales de venta.",
        bold_prefix="Selección y Justificación de K (K=4 vs K=3):"
    )

    # =========================================================================
    # 6. RESULTADOS Y ANÁLISIS
    # =========================================================================
    pdf.add_page()
    pdf.section_title("6", "Resultados y Análisis")

    # Tabla de Centroides formal
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(243, 244, 246)
    pdf.set_text_color(17, 24, 39)
    pdf.set_draw_color(209, 213, 219)
    
    cols_c = [48, 22, 22, 22, 20, 36]
    pdf.cell(cols_c[0], 6, "Clúster Asignado", 1, 0, "C", True)
    pdf.cell(cols_c[1], 6, "Venta Física", 1, 0, "C", True)
    pdf.cell(cols_c[2], 6, "Venta Digital", 1, 0, "C", True)
    pdf.cell(cols_c[3], 6, "Precio Medio", 1, 0, "C", True)
    pdf.cell(cols_c[4], 6, "Calif. Media", 1, 0, "C", True)
    pdf.cell(cols_c[5], 6, "Proporción", 1, 1, "C", True)

    centroides = [
        ("Superventas Globales (Blockbusters)", "8.69 M", "12.00 M", "$69.87 USD", "88.3 pts", "169 (18.4%)"),
        ("Fracasos Comerciales y Bajo Rendimiento", "0.41 M", "0.50 M", "$54.78 USD", "54.1 pts", "224 (24.3%)"),
        ("Coleccionables de Consola (Físico Fuerte)", "6.65 M", "2.50 M", "$59.99 USD", "84.2 pts", "210 (22.8%)"),
        ("Éxitos Digitales e Indies Virales", "0.60 M", "7.80 M", "$34.70 USD", "82.3 pts", "317 (34.5%)")
    ]

    pdf.set_font("Helvetica", "", 7.8)
    pdf.set_text_color(55, 65, 81)
    for c_n, c_f, c_d, c_p, c_ca, c_v in centroides:
        pdf.cell(cols_c[0], 5.5, f" {c_n}", 1, 0, "L")
        pdf.cell(cols_c[1], 5.5, c_f, 1, 0, "C")
        pdf.cell(cols_c[2], 5.5, c_d, 1, 0, "C")
        pdf.cell(cols_c[3], 5.5, c_p, 1, 0, "C")
        pdf.cell(cols_c[4], 5.5, c_ca, 1, 0, "C")
        pdf.cell(cols_c[5], 5.5, f" {c_v}", 1, 1, "C")

    pdf.ln(4)

    # Gráficas de soporte en paralelo (SIN TEXTO 'Figura 3...')
    img_pca = "assets/reporte_videojuegos/3_pca_clusters.png"
    img_box = "assets/reporte_videojuegos/4_boxplot_ventas.png"
    y_g = pdf.get_y()
    if os.path.exists(img_pca) and os.path.exists(img_box):
        pdf.image(img_pca, x=20, y=y_g, w=82)
        pdf.image(img_box, x=108, y=y_g, w=82)
        pdf.ln(58)

    pdf.paragraph(
        "La reducción con PCA en 2 dimensiones retiene el 75.2% de la varianza total de la información (49.9% en PC1 y 25.4% en PC2). "
        "En la proyección bidimensional se comprueba la nitidez de los grupos: los Blockbusters se proyectan hacia el extremo derecho de máxima recaudación, "
        "los Éxitos Digitales en la parte superior de alta descarga, los Coleccionables de Consola en la parte inferior de demanda física, "
        "y los Fracasos Comerciales agrupados de manera compacta en la esquina inferior izquierda.",
        bold_prefix="Interpretación de los Agrupamientos:"
    )

    # =========================================================================
    # 7. DASHBOARD
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

    # Imagen de dona (SIN TEXTO 'Figura 4...')
    img_dona = "assets/reporte_videojuegos/5_dona_proporcion.png"
    if os.path.exists(img_dona):
        pdf.image(img_dona, x=65, y=pdf.get_y(), w=80)
        pdf.ln(70)

    # =========================================================================
    # 8. CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    pdf.add_page()
    pdf.section_title("8", "Conclusiones y Recomendaciones")

    pdf.paragraph("Hallazgos Principales:")
    pdf.bullet("1. Predominancia del Canal Digital", "El 34.5% de los videojuegos (Éxitos Digitales) vende 13 veces más por descarga digital que en formato físico (7.80 M vs. 0.60 M). Producir discos físicos para estos juegos representa una pérdida financiera directa.")
    pdf.bullet("2. Concentración de Rentabilidad", "Menos del 20% del catálogo (Superventas Blockbusters) genera más de la mitad de los ingresos comerciales brutos globales.")
    pdf.bullet("3. Tasa de Falla en Tiendas", "El 24.3% de los títulos lanzados es un fracaso comercial con ventas inferiores a 1 millón y calificaciones bajas (54 puntos), siendo el principal causante de inventario muerto.")

    pdf.paragraph("Recomendaciones para la Toma de Decisiones:")
    pdf.bullet("1. Política Cero Discos Físicos para Indies", "Comercializar los juegos del Clúster de Éxitos Digitales exclusivamente por internet, ahorrando el 100% de los costos de manufactura plástica y fletes.")
    pdf.bullet("2. Producción Focalizada en Coleccionables", "Concentrar la impresión de cajas y ediciones especiales únicamente en juegos de consola de aventura y plataformas (Clúster de Coleccionables).")
    pdf.bullet("3. Remates Rápidos para Títulos de Bajo Rendimiento", "Aplicar descuentos agresivos durante las primeras cuatro semanas para los títulos del Clúster de Fracasos, recuperando liquidez antes de que su valor comercial decaiga totalmente.")

    pdf.paragraph(
        "K-Means presupone grupos hiper-esféricos de varianza similar y no contempla variaciones estacionales (ofertas de fin de año o Black Friday). "
        "Como trabajo futuro, se recomienda integrar modelos temporales y algoritmos basados en densidad como DBSCAN.",
        bold_prefix="Limitaciones del Modelo:"
    )

    output_path = "docs/Documentacion_Oficial_Proyecto_KMeans_Videojuegos.pdf"
    os.makedirs("docs", exist_ok=True)
    pdf.output(output_path)
    print(f"Documento oficial limpio sin encabezados, sin pies y sin leyendas generado: {output_path}")

if __name__ == "__main__":
    build_clean_documentation_pdf()
