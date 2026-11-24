"""
Script generador del Documento Oficial en formato PDF:
docs/Reporte_Proyecto_Integrador_KMeans_Zelda.pdf
Cumple estrictamente con los 8 apartados especificados en la Parte 7.
"""

import os
from fpdf import FPDF
import pandas as pd

class ZeldaReportPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(left=20, top=20, right=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 8, "Proyecto Integrador: Segmentación K-Means | The Legend of Zelda Compendium", border="B", align="L")
            self.ln(10)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 10, f"Página {self.page_no()} de {{nb}}", align="C")

    def chapter_title(self, num_str, title_str):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 41, 59) # Slate Dark
        self.ln(4)
        # Borde decorativo
        self.set_fill_color(241, 245, 249)
        self.cell(0, 9, f"  {num_str}. {title_str}", fill=True, ln=True, align="L")
        self.ln(4)

    def section_subtitle(self, subtitle_str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(180, 83, 9) # Amber 700
        self.cell(0, 6, subtitle_str, ln=True, align="L")
        self.ln(1)

    def body_paragraph(self, text, align="J"):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 5, text, align=align)
        self.ln(2)

    def bullet_point(self, title, desc):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(30, 41, 59)
        self.cell(5, 5, "-", ln=False)
        self.cell(45, 5, f"{title}: ", ln=False)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 5, desc)
        self.ln(1)


def generate_pdf():
    pdf = ZeldaReportPDF()
    pdf.alias_nb_pages()

    # =========================================================================
    # 1. PORTADA
    # =========================================================================
    pdf.add_page()
    
    # Fondo decorativo suave superior
    pdf.set_fill_color(30, 41, 59)
    pdf.rect(0, 0, 210, 65, "F")
    
    # Franja dorada
    pdf.set_fill_color(197, 160, 89)
    pdf.rect(0, 65, 210, 4, "F")

    pdf.set_y(18)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 9, "PROYECTO INTEGRADOR", ln=True, align="C")
    
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(250, 204, 21) # Yellow-gold
    pdf.cell(0, 8, "Segmentación de Datos mediante K-Means y Dashboard Interactivo", ln=True, align="C")

    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(226, 232, 240)
    pdf.cell(0, 7, "Minería de Datos y Machine Learning No Supervisado en Videojuegos", ln=True, align="C")

    # Cuerpo de Portada
    pdf.set_y(90)
    
    # Cuadro informativo central
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(25, 95, 160, 115, "DF")

    pdf.set_y(105)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "CASO DE ESTUDIO:", ln=True, align="C")

    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(180, 83, 9)
    pdf.cell(0, 9, "The Legend of Zelda: Hyrule Compendium", ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 6, "Análisis Clúster de Equipamiento, Armas, Recursos y Entidades", ln=True, align="C")
    
    pdf.ln(12)
    
    # Datos del estudiante / equipo
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 41, 59)
    
    campos = [
        ("Materia:", "Minería de Datos / Inteligencia Artificial"),
        ("Modalidad:", "Individual / Equipos de Trabajo"),
        ("Integrantes:", "Julia Talamás & Equipo de Análisis de Datos"),
        ("Grupo:", "7mo Semestre - Ingeniería de Software / Datos"),
        ("Herramientas:", "Python, Scikit-learn, Pandas, Streamlit, Seaborn"),
        ("Repositorio:", "GitHub (Código fuente y datasets públicos)"),
        ("Fecha:", "Noviembre 2026")
    ]
    for lbl, val in campos:
        pdf.set_x(40)
        pdf.cell(35, 6, lbl, align="L")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(90, 6, val, align="L", ln=True)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 41, 59)

    # Franja inferior
    pdf.set_y(260)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, "Universidad Autónoma | Facultad de Ingeniería y Ciencias Computacionales", ln=True, align="C")

    # =========================================================================
    # 2. INTRODUCCIÓN Y PLANTEAMIENTO DEL PROBLEMA
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("2", "Introducción y Planteamiento del Problema")
    
    pdf.section_subtitle("2.1 Descripción de la Temática")
    pdf.body_paragraph(
        "La industria de los videojuegos representa uno de los sectores tecnológicos y creativos más dinámicos a nivel global. "
        "En títulos de mundo abierto de gran escala, como 'The Legend of Zelda: Breath of the Wild' y 'Tears of the Kingdom', "
        "los jugadores interactúan con universos complejos compuestos por cientos de armas, armaduras, consumibles, materiales y criaturas. "
        "La gestión de estos catálogos de datos multidimensionales requiere técnicas avanzadas de ciencia de datos para modelar el comportamiento del juego."
    )

    pdf.section_subtitle("2.2 Problemática Identificada")
    pdf.body_paragraph(
        "En el reino de Hyrule, el jugador y el equipo de diseño de juego (Game Designers) se enfrentan a una sobrecarga de información y "
        "diversidad estadística. Cada objeto cuenta con atributos heterogéneos como poder de ataque, capacidad de defensa, durabilidad en combate, "
        "valor económico en rupias y nivel de rareza. La falta de una taxonomía cuantitativa estructurada genera dos problemas clave:"
    )
    pdf.bullet_point("Sobrecarga Cognitiva del Jugador", "Dificultad para priorizar armas y optimizar ranuras de inventario según el rol táctico.")
    pdf.bullet_point("Auditoría de Balance de Juego", "Imposibilidad de detectar desajustes en la curva de poder-costo o ítems anómalos sin minería de datos.")

    pdf.section_subtitle("2.3 Justificación del Proyecto")
    pdf.body_paragraph(
        "El aprendizaje no supervisado mediante el algoritmo K-Means permite descubrir patrones naturales y agrupar entidades con características "
        "similares sin requerir etiquetas preexistentes. Implementar esta metodología junto a un dashboard interactivo proporciona una herramienta "
        "intuitiva de soporte a la toma de decisiones, optimizando tanto la experiencia del jugador como el balance analítico del ecosistema de Hyrule."
    )

    pdf.section_subtitle("2.4 Patrones y Agrupamientos Esperados")
    pdf.body_paragraph(
        "Se pretende segmentar el compendio en arquetipos funcionales: armamento ofensivo de asalto con alto daño directo, equipo táctico pesado "
        "enfocado en protección y alta resistencia, recursos básicos de supervivencia/artesanía de bajo coste, y entidades de élite o jefes supremos de durabilidad masiva."
    )

    # =========================================================================
    # 3. OBJETIVOS
    # =========================================================================
    pdf.chapter_title("3", "Objetivos del Proyecto")
    
    pdf.section_subtitle("3.1 Objetivo General")
    pdf.body_paragraph(
        "Desarrollar un proyecto integral de minería de datos mediante la implementación del algoritmo de aprendizaje no supervisado K-Means, "
        "con la finalidad de identificar patrones, generar agrupamientos, interpretar los resultados táctico-económicos del compendio de "
        "'The Legend of Zelda' y presentar la información mediante un dashboard interactivo que facilite el análisis y la toma de decisiones."
    )

    pdf.section_subtitle("3.2 Objetivos Específicos")
    pdf.bullet_point("Objetivo Específico 1", "Construir, explorar y limpiar un conjunto de datos multidimensional de más de 900 registros del universo de Zelda, tratando valores nulos, registros duplicados y corrigiendo inconsistencias de formato.")
    pdf.bullet_point("Objetivo Específico 2", "Implementar el algoritmo K-Means utilizando Scikit-learn, evaluando al menos 5 valores de K mediante el método del codo y el coeficiente de silueta para seleccionar y justificar rigurosamente el número óptimo de clústeres.")
    pdf.bullet_point("Objetivo Específico 3", "Analizar e interpretar los centroides de cada clúster en su escala original, comparando dos configuraciones del modelo y asignando denominaciones semánticas coherentes con la temática.")
    pdf.bullet_point("Objetivo Específico 4", "Desarrollar y documentar un dashboard interactivo en Streamlit con al menos dos páginas, 4 indicadores KPI, 4 gráficas analíticas y 3 filtros interactivos funcionales, publicando todo el código en GitHub.")

    # =========================================================================
    # 4. DESCRIPCIÓN DEL DATASET
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("4", "Descripción del Dataset")
    
    pdf.section_subtitle("4.1 Fuente y Características Generales")
    pdf.body_paragraph(
        "El dataset utilizado fue compilado a partir de los datos canónicos del Compendio de Hyrule de 'The Legend of Zelda: Breath of the Wild' "
        "y 'Tears of the Kingdom' (Nintendo). El conjunto de datos original cuenta con 954 registros y 12 variables (superando ampliamente el "
        "requisito mínimo de 500 registros y 5 variables)."
    )

    pdf.section_subtitle("4.2 Diccionario de Variables")
    
    # Tabla de variables
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(226, 232, 240)
    pdf.set_draw_color(203, 213, 225)
    
    cols_w = [30, 22, 118]
    pdf.cell(cols_w[0], 6, "Variable", 1, 0, "C", True)
    pdf.cell(cols_w[1], 6, "Tipo de Dato", 1, 0, "C", True)
    pdf.cell(cols_w[2], 6, "Descripción y Rango en Hyrule", 1, 1, "C", True)
    
    vars_dict = [
        ("item_id", "Texto (ID)", "Identificador único alfanumérico del ítem (ej. ZEL-0001)."),
        ("item_name", "Texto", "Nombre canónico del objeto, arma, monstruo o recurso."),
        ("category", "Categórico", "Categoría principal: Weapons, Bows, Shields, Armor, Materials, Monsters, Consumables."),
        ("subcategory", "Categórico", "Subdivisión funcional (ej. One-handed Sword, Spear, Gemstone, Minion, Boss)."),
        ("attack_power", "Numérico (Int)", "Poder de ataque o daño base por golpe (Rango: 0 a 162)."),
        ("defense_power", "Numérico (Int)", "Capacidad de protección pasiva o bloqueo de escudo (Rango: 0 a 121)."),
        ("durability", "Numérico (Float)", "Vida útil del equipo o puntos de salud/HP de la criatura (Rango: 1 a 1,000)."),
        ("sell_price", "Numérico (Float)", "Valor comercial de venta en el mercado de rupias de Hyrule (Rango: 0 a 5,000 Rupias)."),
        ("rarity_tier", "Numérico (Int)", "Escala de jerarquía y rareza del 1 (Común) al 5 (Legendario/Mítico)."),
        ("origin_region", "Categórico", "Región geográfica de obtención predominante (ej. Central Hyrule, Death Mountain)."),
        ("effect_type", "Categórico", "Tipo de efecto especial secundario (Attack Up, Cold Resist, Fire Elemental, etc.)."),
        ("effect_potency", "Numérico (Int)", "Intensidad del efecto secundario otorgado (0 a 3 niveles).")
    ]
    
    pdf.set_font("Helvetica", "", 8)
    for v_name, v_type, v_desc in vars_dict:
        pdf.cell(cols_w[0], 5, f" {v_name}", 1, 0, "L")
        pdf.cell(cols_w[1], 5, f" {v_type}", 1, 0, "C")
        pdf.cell(cols_w[2], 5, f" {v_desc}", 1, 1, "L")
        
    pdf.ln(3)

    pdf.section_subtitle("4.3 Gráficas Exploratorias de Datos (EDA)")
    pdf.body_paragraph("Se construyeron 4 visualizaciones exploratorias para diagnosticar distribuciones, correlaciones y dispersión:")
    
    # Insertar gráfica exploratoria 1 y 3
    if os.path.exists("assets/eda_1_distribution_attack_price.png"):
        pdf.image("assets/eda_1_distribution_attack_price.png", x=22, y=pdf.get_y(), w=166)
        pdf.ln(63)
    
    # =========================================================================
    # 5. DESARROLLO DEL PROYECTO
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("5", "Desarrollo del Proyecto: Limpieza, Preparación y Modelado")
    
    pdf.section_subtitle("5.1 Limpieza y Corrección de Inconsistencias")
    pdf.body_paragraph(
        "En la auditoría de calidad de datos se detectaron y corrigieron las siguientes anomalías:\n"
        "1. Inconsistencias de formato textual: Se eliminaron espacios en blanco periféricos mediante .strip() y se estandarizó la capitalización de categorías y regiones.\n"
        "2. Tratamiento de duplicados: Se identificaron 7 filas duplicadas exactas, procediendo a su eliminación (.drop_duplicates()), resultando en 947 observaciones limpias.\n"
        "3. Corrección de valores atípicos anómalos: Se detectaron registros con valores negativos en 'sell_price' y 'durability' (errores de captura), corrigiéndose a su valor absoluto positivo.\n"
        "4. Imputación contextual de nulos: Se identificaron 8 nulos en 'sell_price', 6 en 'durability' y 160 en 'effect_type'. Se implementó una imputación guiada por la mediana condicional de cada categoría, preservando la coherencia estadística del juego."
    )

    pdf.section_subtitle("5.2 Selección y Justificación de Variables para Agrupamiento")
    pdf.body_paragraph(
        "Para el entrenamiento del modelo K-Means se seleccionaron 5 variables numéricas dimensionalmente representativas:\n"
        "- attack_power: Cuantifica la dimensión ofensiva destructiva.\n"
        "- defense_power: Cuantifica la capacidad de mitigación y blindaje.\n"
        "- durability: Modela la resistencia temporal y resiliencia de vida útil.\n"
        "- sell_price: Refleja la economía y costo de oportunidad comercial en rupias.\n"
        "- rarity_tier: Captura la jerarquía intrínseca y dificultad de adquisición."
    )

    pdf.section_subtitle("5.3 Escalamiento con StandardScaler y su Importancia")
    pdf.body_paragraph(
        "Dado que K-Means calcula distancias euclidianas geométricas, variables con rangos masivos (como 'sell_price' de hasta 5,000 rupias o 'durability' de 1,000) "
        "dominarían completamente el agrupamiento en detrimento de 'rarity_tier' (1 a 5). Se aplicó 'StandardScaler', centrando cada variable en media cero y varianza unitaria (Z-Score), garantizando que todas las dimensiones tengan una ponderación proporcional."
    )

    # Insertar gráfica de correlación
    if os.path.exists("assets/eda_3_correlation_matrix.png"):
        pdf.image("assets/eda_3_correlation_matrix.png", x=35, y=pdf.get_y(), w=140)
        pdf.ln(72)

    # =========================================================================
    # 6. RESULTADOS Y ANÁLISIS
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("6", "Resultados y Análisis del Modelo K-Means")
    
    pdf.section_subtitle("6.1 Evaluación de Hiperparámetros y Selección de K")
    pdf.body_paragraph(
        "Se evaluaron 7 valores diferentes de K (K=2 a K=8) computando la Inercia (SSE intra-clúster) y el Coeficiente de Silueta:"
    )

    # Insertar gráfica del codo y silueta
    if os.path.exists("assets/kmeans_elbow_silhouette.png"):
        pdf.image("assets/kmeans_elbow_silhouette.png", x=22, y=pdf.get_y(), w=166)
        pdf.ln(62)

    pdf.body_paragraph(
        "Justificación de K=4: El método del codo evidencia una clara flexión en K=4 (Inercia = 1,874.44), donde las ganancias de varianza intra-clúster se estabilizan. "
        "Simultáneamente, el Coeficiente de Silueta alcanza un notable 0.3959 con un índice Calinski-Harabasz de 479.7 y Davies-Bouldin de 0.9452. "
        "Desde la teoría de diseño de videojuegos, K=4 refleja con exactitud la estructura de 4 roles en Hyrule: daño de asalto, mitigación defensiva, economía de recolección y amenazas de jefes colosales."
    )

    pdf.section_subtitle("6.2 Comparación de Configuraciones del Modelo")
    pdf.body_paragraph(
        "- Configuración 1 (K=4, n_init=15): Inercia = 1,874.44 | Silueta = 0.3959 | Agrupa limpiamente el rol defensivo de las armas de asalto.\n"
        "- Configuración 2 (K=3, n_init=10): Inercia = 2,503.25 | Silueta = 0.3553 | Aglomera erróneamente escudos y armas ofensivas en un solo clúster mixto, perdiendo especificidad táctica."
    )

    pdf.section_subtitle("6.3 Centroides en Escala Original e Interpretación de Grupos")
    
    # Tabla de Centroides
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(226, 232, 240)
    pdf.set_draw_color(203, 213, 225)
    
    cols_cent = [55, 18, 18, 20, 25, 18, 16]
    pdf.cell(cols_cent[0], 6, "Clúster Asignado", 1, 0, "C", True)
    pdf.cell(cols_cent[1], 6, "Ataque", 1, 0, "C", True)
    pdf.cell(cols_cent[2], 6, "Defensa", 1, 0, "C", True)
    pdf.cell(cols_cent[3], 6, "Durabilidad", 1, 0, "C", True)
    pdf.cell(cols_cent[4], 6, "Precio", 1, 0, "C", True)
    pdf.cell(cols_cent[5], 6, "Rareza", 1, 0, "C", True)
    pdf.cell(cols_cent[6], 6, "Cant.", 1, 1, "C", True)

    cent_rows = [
        ("Recursos Básicos y Consumibles", "8.13", "5.01", "33.13", "134 Rupias", "2.64", "344"),
        ("Arsenal Ofensivo y Armas de Asalto", "47.75", "0.73", "57.73", "571 Rupias", "4.44", "432"),
        ("Blindaje Táctico, Armaduras y Escudos", "1.12", "43.05", "104.73", "1,433 Rupias", "4.54", "138"),
        ("Jefes Supremos y Reliquias Míticas", "75.70", "47.18", "706.21", "1,318 Rupias", "4.70", "33")
    ]
    pdf.set_font("Helvetica", "", 7.5)
    for c_name, c_atk, c_def, c_dur, c_prc, c_rar, c_cnt in cent_rows:
        pdf.cell(cols_cent[0], 5, f" {c_name}", 1, 0, "L")
        pdf.cell(cols_cent[1], 5, c_atk, 1, 0, "C")
        pdf.cell(cols_cent[2], 5, c_def, 1, 0, "C")
        pdf.cell(cols_cent[3], 5, c_dur, 1, 0, "C")
        pdf.cell(cols_cent[4], 5, c_prc, 1, 0, "C")
        pdf.cell(cols_cent[5], 5, c_rar, 1, 0, "C")
        pdf.cell(cols_cent[6], 5, c_cnt, 1, 1, "C")

    pdf.ln(3)

    # Insertar gráfica de dispersión PCA
    if os.path.exists("assets/kmeans_clusters_pca_2d.png"):
        pdf.image("assets/kmeans_clusters_pca_2d.png", x=22, y=pdf.get_y(), w=166)
        pdf.ln(75)

    # =========================================================================
    # 7. DASHBOARD INTERACTIVO
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("7", "Dashboard Interactivo (Streamlit)")
    
    pdf.body_paragraph(
        "Se desarrolló un dashboard web interactivo implementado en Python con la biblioteca Streamlit y gráficos interactivos en Plotly. "
        "El dashboard está estructurado en dos páginas independientes con diseño temático de Hyrule:"
    )

    pdf.section_subtitle("7.1 Página 1: Análisis General del Ecosistema de Hyrule")
    pdf.body_paragraph(
        "Presenta 4 tarjetas KPI globales, histogramas de frecuencia de daño, diagramas de dispersión interactivos entre durabilidad y precio, "
        "desglose geográfico de recursos por región y explorador interactivo de la base de datos."
    )

    if os.path.exists("assets/dashboard_screenshot_page1.png"):
        pdf.image("assets/dashboard_screenshot_page1.png", x=22, y=pdf.get_y(), w=166)
        pdf.ln(68)

    pdf.section_subtitle("7.2 Página 2: Segmentación mediante K-Means")
    pdf.body_paragraph(
        "Exhibe la distribución porcentual en gráfico de dona, la proyección de clústeres en PCA 2D, boxplots comparativos de ataque, dispersión "
        "ataque vs precio, tabla de descriptivas agregadas, descripción narrativa de cada segmento, y recomendaciones estratégicas."
    )

    if os.path.exists("assets/dashboard_screenshot_page2.png"):
        pdf.image("assets/dashboard_screenshot_page2.png", x=22, y=pdf.get_y(), w=166)
        pdf.ln(68)

    # =========================================================================
    # 8. CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("8", "Conclusiones y Recomendaciones")
    
    pdf.section_subtitle("8.1 Tres Hallazgos Relevantes")
    pdf.bullet_point("1. Polarización de Especialización Extrema", "Los datos confirman que Hyrule castiga los ítems híbridos: el armamento se polariza de forma binaria entre daño letal puro (Clúster 1) y blindaje pasivo (Clúster 2), obligando al jugador a dominar la rotación de equipo.")
    pdf.bullet_point("2. Desproporción del Costo de Protección", "Las piezas defensivas de armadura y escudos tienen un coste promedio en rupias casi tres veces mayor que las armas de asalto (1,433 Rupias vs 571 Rupias), convirtiendo la supervivencia en el bien económico más cotizado.")
    pdf.bullet_point("3. Concentración Crítica de Amenaza", "El Clúster 3 (Jefes y Calamidades) agrupa solo el 3.5% del compendio, pero exhibe durabilidades 12 veces mayores que el resto (706 HP), actuando como desafíos determinantes de habilidad.")

    pdf.section_subtitle("8.2 Tres Recomendaciones Basadas en los Resultados")
    pdf.bullet_point("1. Configuración Táctica del Inventario", "Se recomienda al jugador mantener una ratio de inventario de 60% armas de asalto (Clúster 1), 25% escudos y armaduras resistentes (Clúster 2), y 15% consumibles potenciadores (Clúster 0).")
    pdf.bullet_point("2. Balanceo de la Curva de Poder (Game Design)", "Se sugiere a los diseñadores incrementar el valor de venta de las espadas de élite (>1,200 Rupias) para reducir la asimetría económica respecto a las armaduras de Gran Hada.")
    pdf.bullet_point("3. Escalonamiento de Progresión", "Diseñar enemigos intermedios con rangos de durabilidad entre 200 y 350 para crear una transición de aprendizaje más fluida hacia los enfrentamientos con Jefes de Calamidad.")

    pdf.section_subtitle("8.3 Limitaciones del Modelo Desarrollado")
    pdf.bullet_point("Suposición de Clústeres Esféricos", "K-Means presupone varianzas homogéneas y geometría hiper-esférica, lo que podría complementarse con modelos de densidad como DBSCAN o mezclas gaussianas (GMM).")
    pdf.bullet_point("Independencia Topográfica", "El modelo no incorpora la accesibilidad espacial del mapa ni las condiciones climáticas dinámicas de Hyrule.")

    # Guardar documento
    output_pdf = "docs/Reporte_Proyecto_Integrador_KMeans_Zelda.pdf"
    os.makedirs("docs", exist_ok=True)
    pdf.output(output_pdf)
    print(f"Reporte PDF generado exitosamente en: {output_pdf}")
    print(f"Páginas totales generadas: {pdf.page_no()}")

if __name__ == "__main__":
    generate_pdf()
