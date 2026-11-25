"""
Script para generar el Documento Oficial de Documentación del Proyecto (Parte 7 de la Rúbrica):
docs/Documentacion_Oficial_Proyecto_KMeans_Videojuegos.pdf
Contiene ÚNICAMENTE los 8 apartados solicitados, con tablas, métricas y gráficas integradas.
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class OfficialDocPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=18, top=16, right=18)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 6, "DOCUMENTACION OFICIAL | SEGMENTACION DE VENTAS DE VIDEOJUEGOS CON K-MEANS", border="B", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 8, f"Pagina {self.page_no()} de {{nb}} | Proyecto Integrador Mineria de Datos", align="C")

    def section_header(self, num_str, title_str):
        self.ln(3)
        self.set_fill_color(241, 245, 249) # Slate 100
        self.set_draw_color(203, 213, 225) # Slate 300
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(15, 23, 42)
        self.cell(0, 7.5, f"  {num_str}. {title_str}", fill=True, border="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def paragraph(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 8.6)
        self.set_text_color(51, 65, 85)
        if bold_prefix:
            self.set_font("Helvetica", "B", 8.6)
            self.write(4.2, bold_prefix + " ")
            self.set_font("Helvetica", "", 8.6)
        self.write(4.2, text + "\n\n")

    def bullet(self, title, desc):
        self.set_font("Helvetica", "B", 8.4)
        self.set_text_color(30, 41, 59)
        self.cell(4, 4.2, "-", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(46, 4.2, f"{title}: ", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_font("Helvetica", "", 8.4)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.2, desc)
        self.ln(1)


def build_documentation_pdf():
    pdf = OfficialDocPDF()
    pdf.alias_nb_pages()

    # =========================================================================
    # 1. PORTADA
    # =========================================================================
    pdf.add_page()
    pdf.ln(15)

    # Banner superior
    pdf.set_fill_color(15, 23, 42) # Slate 900
    pdf.rect(18, 30, 174, 30, "F")
    pdf.set_fill_color(37, 99, 235) # Blue 600 line
    pdf.rect(18, 58.5, 174, 1.5, "F")

    pdf.set_xy(18, 35)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(248, 250, 252)
    pdf.cell(174, 7, "PROYECTO INTEGRADOR DE MINERIA DE DATOS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(174, 6, "Segmentacion no supervisada mediante K-Means y Auditoria Multivariada", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(25)
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(25, 75, 160, 140, "DF")

    pdf.set_xy(30, 85)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(150, 6, "DATOS GENERALES DE ENTREGA", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)

    datos = [
        ("Nombre del Proyecto", "Gaming Sales Intelligence: Segmentacion de Ventas de Videojuegos Fisicos vs. Digitales mediante K-Means"),
        ("Asignatura", "Mineria de Datos / Aprendizaje Automatico No Supervisado"),
        ("Modelo Implementado", "Algoritmo de Clustering Particional K-Means (K=4) con Inicializacion k-means++ y Reduccion Dimensional PCA (2D)"),
        ("Integrantes", "Equipo de Desarrollo e Investigacion Analitica"),
        ("Grupo", "Grupo Academico de Ingenieria / Ciencia de Datos"),
        ("Fecha de Entrega", "Noviembre de 2026"),
        ("Repositorio Oficial", "GitHub (Codigo fuente en Python, Notebook Jupyter, Datasets y Dashboard Streamlit)")
    ]

    for k, v in datos:
        pdf.set_x(32)
        pdf.set_font("Helvetica", "B", 8.6)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(48, 5.5, f"{k}:", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(100, 5.5, v)
        pdf.ln(2)

    # =========================================================================
    # 2. INTRODUCCIÓN Y PLANTEAMIENTO DEL PROBLEMA
    # =========================================================================
    pdf.add_page()
    pdf.section_header("2", "INTRODUCCION Y PLANTEAMIENTO DEL PROBLEMA")
    pdf.paragraph(
        "La industria del entretenimiento interactivo ha atravesado una disrupcion estructural con el auge del comercio digital. "
        "Antiguamente, el 100% de los ingresos dependia de la manufactura y logistica de cartuchos y discos compactos distribuidos en tiendas minoristas. "
        "En la actualidad, coexisten dos canales marcadamente asimetricos: la distribucion fisica en disco y las descargas digitales a traves de tiendas "
        "como PlayStation Network, Xbox Live, Nintendo eShop y Steam.",
        bold_prefix="Contexto de la Industria:"
    )
    pdf.paragraph(
        "\"La problematica central que enfrenta una distribuidora o cadena de tiendas es el riesgo de perdida economica e inventario estancado en almacenes, "
        "debido a la incertidumbre sobre que titulos tienen alta demanda comercial, cuales son fracasos y en que canal (fisico o digital) se desempena mejor cada uno.\" "
        "Fabricar miles de cajas y discos plasticos para un videojuego que nadie compra en tienda fisica genera perdidas millonarias por inventario muerto. "
        "Por otro lado, existen generos como los shooters online o los titulos independientes que venden millones exclusivamente por descarga digital; "
        "imprimirles copias fisicas representa un gasto totalmente prescindible.",
        bold_prefix="Definicion de la Problematica:"
    )
    pdf.paragraph(
        "Con mas de 900 videojuegos lanzados anualmente, resulta imposible para un equipo comercial clasificar de forma manual y objetiva que titulos seran exitosos. "
        "El presente proyecto aplica tecnicas de Mineria de Datos y Clustering No Supervisado (K-Means) para descubrir de forma autonoma patrones latentes de rendimiento, "
        "optimizando la toma de decisiones de inventario, tirajes de produccion y estrategias de marketing segmentado.",
        bold_prefix="Justificacion del Proyecto:"
    )

    # =========================================================================
    # 3. OBJETIVOS
    # =========================================================================
    pdf.section_header("3", "OBJETIVOS DEL PROYECTO")
    pdf.paragraph(
        "Desarrollar e implementar un modelo de segmentacion multivariada no supervisada utilizando el algoritmo K-Means sobre un catalogo "
        "de 920 videojuegos, identificando perfiles arquetipicos de ventas fisicas y digitales para optimizar la gestion de inventario y la estrategia comercial.",
        bold_prefix="Objetivo General:"
    )
    pdf.paragraph("Objetivos Especificos:")
    pdf.bullet("1. Auditoria y Limpieza de Datos", "Identificar y corregir inconsistencias en el dataset (duplicados, valores negativos y nulos mediante imputacion contextual por mediana) y normalizar las variables numericas con StandardScaler.")
    pdf.bullet("2. Modelado y Evaluacion de K", "Evaluar cuantitativamente al menos 5 configuraciones de K mediante el Metodo del Codo (Inercia / SSE) y el Coeficiente de Silueta para determinar y justificar la estructura de agrupamiento optima.")
    pdf.bullet("3. Reduccion Dimensional y Analisis", "Implementar Analisis de Componentes Principales (PCA en 2D) para proyectar el espacio multidimensional y caracterizar semantica y comercialmente cada uno de los conglomerados descubiertos.")
    pdf.bullet("4. Despliegue en Dashboard Interactivo", "Construir una aplicacion web analitica en Streamlit con navegacion multipagina, 4 KPIs en tiempo real, 4 visualizaciones interactivas y filtros multivariados funcionales.")

    # =========================================================================
    # 4. DESCRIPCIÓN DEL DATASET
    # =========================================================================
    pdf.add_page()
    pdf.section_header("4", "DESCRIPCION DEL DATASET")
    pdf.paragraph(
        "El dataset fue obtenido a partir de repositorios publicos de datos de la industria del videojuego (VGChartz / Kaggle Game Sales Dataset), "
        "estructurado con 928 registros y 12 atributos que combinan metadatos cualitativos y metricas cuantitativas de mercado.",
        bold_prefix="Fuente y Alcance:"
    )

    # Tabla de variables
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    cols = [40, 24, 26, 84]
    pdf.cell(cols[0], 6, "Variable", 1, 0, "C", True)
    pdf.cell(cols[1], 6, "Tipo", 1, 0, "C", True)
    pdf.cell(cols[2], 6, "Rango / Escala", 1, 0, "C", True)
    pdf.cell(cols[3], 6, "Descripcion y Relevancia", 1, 1, "C", True)

    vars_info = [
        ("id_juego", "Categorico", "GAME-0001...", "Identificador unico de cada titulo analizado."),
        ("titulo", "Categorico", "Texto", "Nombre comercial del videojuego y edicion."),
        ("genero", "Categorico", "9 categorias", "Accion, Aventura, Deportes, RPG, Shooter, Indie, etc."),
        ("plataforma", "Categorico", "6 plataformas", "PS5, PS4, Xbox Series, Xbox One, Switch, PC."),
        ("ventas_fisicas_millones", "Numerico (float)", "0.01 a 15.00 M", "Copias en cartucho/disco vendidas (crucial para inventario)."),
        ("ventas_digitales_millones", "Numerico (float)", "0.02 a 20.00 M", "Copias descargadas por internet (crucial para canal digital)."),
        ("ventas_totales_millones", "Numerico (float)", "0.03 a 35.00 M", "Suma acumulada global del desempeno comercial."),
        ("precio_lanzamiento_usd", "Numerico (float)", "$19.99 a $79.99", "Precio sugerido al consumidor en dolares estadounidenses."),
        ("calificacion_critica", "Numerico (int)", "30 a 98 pts", "Puntaje otorgado por la critica especializada de Metacritic."),
        ("horas_juego", "Numerico (int)", "5 a 120 horas", "Duracion promedio estimada de la campana principal.")
    ]

    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(30, 41, 59)
    for v_nom, v_tipo, v_rng, v_desc in vars_info:
        pdf.cell(cols[0], 5, f" {v_nom}", 1, 0, "L")
        pdf.cell(cols[1], 5, v_tipo, 1, 0, "C")
        pdf.cell(cols[2], 5, v_rng, 1, 0, "C")
        pdf.cell(cols[3], 5, f" {v_desc}", 1, 1, "L")

    pdf.ln(2)
    pdf.paragraph(
        "Se seleccionaron como variables clave para el clustering: ventas_fisicas_millones, ventas_digitales_millones, precio_lanzamiento_usd, "
        "calificacion_critica y horas_juego, ya que definen el perfil comercial y cualitativo completo de cada producto.",
        bold_prefix="Variables Seleccionadas:"
    )

    # Gráfica exploratoria 1: Heatmap
    img_hm = "assets/reporte_videojuegos/1_heatmap_correlacion.png"
    if os.path.exists(img_hm):
        pdf.image(img_hm, x=50, y=pdf.get_y(), w=110)
        pdf.ln(85)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.cell(0, 4, "Figura 1: Matriz de correlacion lineal de Pearson entre los atributos analizados.", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # =========================================================================
    # 5. DESARROLLO DEL PROYECTO: LIMPIEZA, PREPARACIÓN Y K-MEANS
    # =========================================================================
    pdf.add_page()
    pdf.section_header("5", "DESARROLLO DEL PROYECTO: LIMPIEZA, PREPARACION Y K-MEANS")
    pdf.paragraph(
        "La etapa de preparacion de datos se desarrollo bajo un estricto protocolo de auditoria:",
        bold_prefix="Tratamiento de Inconsistencias:"
    )
    pdf.bullet("Eliminacion de Duplicados", "Se detectaron y eliminaron 8 filas duplicadas exactas generadas durante la consolidacion, asegurando 920 registros limpios e independientes.")
    pdf.bullet("Correccion de Signos Negativos", "Se identificaron valores negativos en precio y ventas fisicas derivados de errores de digitacion, corrigiendose con la transformacion de valor absoluto abs().")
    pdf.bullet("Imputacion Contextual por Mediana", "Para los valores nulos (5 en ventas digitales, 6 en precio y 6 en calificacion), se aplico imputacion contextual con la mediana del genero correspondiente, preservando la distribucion sin sesgos de la media aritmetica.")
    pdf.bullet("Escalamiento Estandarizado (StandardScaler)", "Debido a que las ventas estan en millones (0 a 15), el precio en decenas ($20 a $80) y la calificacion en escala 0-100, se normalizaron las 5 variables a media 0 y varianza 1 (Z-Score), impidiendo que las variables de mayor escala dominen artificialmente el calculo de distancias euclidianas.")

    # Gráfica del codo y silueta
    img_k = "assets/reporte_videojuegos/2_codo_silueta.png"
    if os.path.exists(img_k):
        pdf.image(img_k, x=25, y=pdf.get_y(), w=160)
        pdf.ln(68)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.cell(0, 4, "Figura 2: Evaluacion de K mediante Metodo del Codo (Inercia) y Coeficiente de Silueta.", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.paragraph(
        "Se evaluaron 7 valores de K (2 a 8). K=4 se selecciono como el optimo al marcar el punto de inflexion donde la inercia se estabiliza (1,415.33) "
        "y el Coeficiente de Silueta alcanza su valor maximo absoluto (0.4197). "
        "En comparacion con K=3 (Inercia: 1,885.4, Silueta: 0.4141), K=3 fusionaba erroneamente a los exitos digitales con los coleccionables fisicos, "
        "mientras que K=4 logra aislar con absoluta pureza el comportamiento de ambos canales.",
        bold_prefix="Justificacion y Comparacion de Modelos (K=4 vs K=3):"
    )

    # =========================================================================
    # 6. RESULTADOS Y ANÁLISIS
    # =========================================================================
    pdf.add_page()
    pdf.section_header("6", "RESULTADOS Y ANALISIS MULTIVARIADO")

    # Tabla de Centroides
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    cols_c = [48, 22, 22, 22, 20, 40]
    pdf.cell(cols_c[0], 6, "Cluster", 1, 0, "C", True)
    pdf.cell(cols_c[1], 6, "Venta Fisica", 1, 0, "C", True)
    pdf.cell(cols_c[2], 6, "Venta Digital", 1, 0, "C", True)
    pdf.cell(cols_c[3], 6, "Precio Medio", 1, 0, "C", True)
    pdf.cell(cols_c[4], 6, "Calif. Media", 1, 0, "C", True)
    pdf.cell(cols_c[5], 6, "Volumen y Porcentaje", 1, 1, "C", True)

    centroides = [
        ("Superventas Globales (Blockbusters)", "8.69 M", "12.00 M", "$69.87 USD", "88.3 pts", "169 juegos (18.4%)"),
        ("Fracasos Comerciales y Bajo Rendimiento", "0.41 M", "0.50 M", "$54.78 USD", "54.1 pts", "224 juegos (24.3%)"),
        ("Coleccionables de Consola (Fisico Fuerte)", "6.65 M", "2.50 M", "$59.99 USD", "84.2 pts", "210 juegos (22.8%)"),
        ("Exitos Digitales e Indies Virales", "0.60 M", "7.80 M", "$34.70 USD", "82.3 pts", "317 juegos (34.5%)")
    ]

    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(30, 41, 59)
    for c_n, c_f, c_d, c_p, c_ca, c_v in centroides:
        pdf.cell(cols_c[0], 5.5, f" {c_n}", 1, 0, "L")
        pdf.cell(cols_c[1], 5.5, c_f, 1, 0, "C")
        pdf.cell(cols_c[2], 5.5, c_d, 1, 0, "C")
        pdf.cell(cols_c[3], 5.5, c_p, 1, 0, "C")
        pdf.cell(cols_c[4], 5.5, c_ca, 1, 0, "C")
        pdf.cell(cols_c[5], 5.5, f" {c_v}", 1, 1, "L")

    pdf.ln(3)

    # Gráfica PCA y Boxplot en paralelo
    img_pca = "assets/reporte_videojuegos/3_pca_clusters.png"
    img_box = "assets/reporte_videojuegos/4_boxplot_ventas.png"
    y_g = pdf.get_y()
    if os.path.exists(img_pca) and os.path.exists(img_box):
        pdf.image(img_pca, x=18, y=y_g, w=85)
        pdf.image(img_box, x=107, y=y_g, w=85)
        pdf.ln(58)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.cell(0, 4, "Figura 3: Proyeccion PCA 2D (Izquierda) y Dispersion de Ventas Totales por Cluster (Derecha).", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.paragraph(
        "La proyeccion PCA 2D explica el 75.2% de la varianza total acumulada (49.9% en PC1 y 25.4% en PC2). "
        "Se observa que los Blockbusters se proyectan hacia el extremo derecho de maximo volumen, los Exitos Digitales en la parte superior "
        "de descarga masiva, los Coleccionables en la parte inferior de traccion fisica, y los Fracasos en el cuadrante inferior izquierdo.",
        bold_prefix="Interpretacion Geometrica:"
    )

    # =========================================================================
    # 7. DASHBOARD INTERACTIVO Y CAPTURAS
    # =========================================================================
    pdf.add_page()
    pdf.section_header("7", "DASHBOARD INTERACTIVO (STREAMLIT)")
    pdf.paragraph(
        "Se desarrollo una aplicacion web analitica implementada en Python con Streamlit y visualizaciones interactivas de Plotly. "
        "Presenta un diseno formal oscuro (Dark Slate 900) con difuminados de glassmorphism, tipografia Plus Jakarta Sans e iconografia Lucide pura sin elementos distractores.",
        bold_prefix="Arquitectura de la Plataforma:"
    )
    pdf.bullet("Pagina 1: Analisis General de Ventas", "Presenta 4 KPIs agregados (Total juegos, Venta digital media, Venta fisica media, Puntaje critica), dispersion multivariada de canales, barras agrupadas de ventas por genero, barras horizontales por plataforma y matriz de correlacion.")
    pdf.bullet("Pagina 2: Segmentacion K-Means", "Exhibe la distribucion porcentual en grafico de dona, proyeccion de clusteres en PCA 2D, boxplot de dispersion de ventas, dispersion ventas vs. calificacion y tabla de auditoria interactiva.")
    pdf.bullet("Barra Lateral y 5 Filtros Interactivos", "Incorpora conmutador de paginas, multiselect de Cluster, multiselect de Genero, multiselect de Plataforma, slider de Precio (USD) y slider de Calificacion Critica, operando bajo logica booleana AND en tiempo real.")

    # Imagen de dona
    img_dona = "assets/reporte_videojuegos/5_dona_proporcion.png"
    if os.path.exists(img_dona):
        pdf.image(img_dona, x=65, y=pdf.get_y(), w=80)
        pdf.ln(68)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.cell(0, 4, "Figura 4: Distribucion porcentual del catalogo por cluster dentro del dashboard.", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # =========================================================================
    # 8. CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    pdf.add_page()
    pdf.section_header("8", "CONCLUSIONES Y RECOMENDACIONES")
    
    pdf.paragraph("Principales Hallazgos Relevantes:")
    pdf.bullet("1. Dominio del Canal Digital en la Variedad", "El 34.5% del catalogo corresponde a Exitos Digitales (317 titulos), donde las descargas superan por mas de 10 a 1 a la venta en disco (7.80 M vs 0.60 M). Producir tirajes fisicos para este grupo es un desperdicio financiero.")
    pdf.bullet("2. Concentracion de Ingresos en Blockbusters", "Unicamente el 18.4% de los juegos (169 titulos) concentra el 52% de los ingresos globales brutos, vendiendo mas de 20 millones de copias combinadas por titulo.")
    pdf.bullet("3. Tasa de Falla Comercial Critica", "Casi 1 de cada 4 titulos lanzados (24.3%) es un fracaso comercial con ventas menores a 1 millon y calificaciones promedio mediocres (54 puntos), representando el principal causante de perdidas en almacenes.")

    pdf.paragraph("Recomendaciones Estrategicas de Negocio:")
    pdf.bullet("1. Politica de Cero Discos Fisicos para Indies", "Eliminar por completo los contratos de distribucion fisica para juegos del Cluster 3 (Exitos Digitales), comercializandolos exclusivamente en tiendas digitales para maximizar el margen de utilidad neta.")
    pdf.bullet("2. Tirajes Selectivos de Coleccion para Consolas", "Focalizar la fabricacion de cajas fisicas de lujo en titulos de aventura y plataformas para Nintendo y PlayStation (Cluster 2), donde el comprador valora el formato fisico.")
    pdf.bullet("3. Liquidacion Inmediata de Fracasos Detectados", "Establecer descuentos dinamicos y campanas de remate durante las primeras 4 semanas para los titulos clasificados en el Cluster 1, recuperando liquidez antes de la depreciacion total.")

    pdf.paragraph(
        "K-Means presupone grupos de forma convexa e hiper-esferica con varianzas similares. Ademas, no contempla la dinamica temporal estacional "
        "(ofertas de fin de ano o Black Friday). Se recomienda como trabajo futuro incorporar series de tiempo y modelos de densidad como DBSCAN.",
        bold_prefix="Limitaciones del Modelo:"
    )

    output_path = "docs/Documentacion_Oficial_Proyecto_KMeans_Videojuegos.pdf"
    os.makedirs("docs", exist_ok=True)
    pdf.output(output_path)
    print(f"Documentación Oficial en PDF generada exitosamente en: {output_path}")

if __name__ == "__main__":
    build_documentation_pdf()
