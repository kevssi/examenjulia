"""
Script para compilar la Guía de Estudio y Defensa en un documento PDF claro, estético y formal:
docs/Guia_Estudio_Defensa_Examen.pdf
"""

import os
from fpdf import FPDF

class StudyGuidePDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=18, top=16, right=18)

    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 6, "GUIA DE ESTUDIO Y DEFENSA ORAL | PROYECTO INTEGRADOR K-MEANS", border="B", align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 8, f"Pagina {self.page_no()} de {{nb}}", align="C")

    def card_banner(self, title, subtitle):
        self.set_fill_color(15, 23, 42) # Slate 900
        self.rect(18, self.get_y(), 174, 22, "F")
        self.set_fill_color(37, 99, 235) # Blue 600 line
        self.rect(18, self.get_y() + 21, 174, 1.5, "F")
        
        self.set_y(self.get_y() + 3)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(248, 250, 252)
        self.cell(0, 6, title, align="C", ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(148, 163, 184)
        self.cell(0, 5, subtitle, align="C", ln=True)
        self.ln(6)

    def section_header(self, num_str, title_str):
        self.ln(2)
        self.set_fill_color(241, 245, 249) # Light grey-blue
        self.set_draw_color(203, 213, 225)
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(15, 23, 42)
        self.cell(0, 7.5, f"  {num_str}. {title_str}", fill=True, border="L", ln=True)
        self.ln(2)

    def paragraph(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 8.8)
        self.set_text_color(51, 65, 85)
        if bold_prefix:
            self.set_font("Helvetica", "B", 8.8)
            self.write(4.5, bold_prefix + " ")
            self.set_font("Helvetica", "", 8.8)
        self.write(4.5, text + "\n\n")

    def bullet(self, title, desc):
        self.set_font("Helvetica", "B", 8.6)
        self.set_text_color(30, 41, 59)
        self.cell(4, 4.5, "-", ln=False)
        self.cell(38, 4.5, f"{title}: ", ln=False)
        self.set_font("Helvetica", "", 8.6)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.5, desc)
        self.ln(1)

    def qa_card(self, question, answer):
        self.set_fill_color(248, 250, 252)
        self.set_draw_color(226, 232, 240)
        
        # Guardar posición
        y_start = self.get_y()
        self.set_font("Helvetica", "B", 8.8)
        self.set_text_color(180, 83, 9) # Amber 700
        self.cell(0, 5, f"Pregunta: {question}", ln=True)
        
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.2, f"Respuesta: {answer}")
        self.ln(2.5)

def build_pdf():
    pdf = StudyGuidePDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Banner superior
    pdf.card_banner(
        "GUIA DE ESTUDIO Y DEFENSA DE PROYECTO",
        "Mineria de Datos | Segmentacion K-Means | The Legend of Zelda Compendium"
    )

    # 1. QUE ES ESTE PROYECTO
    pdf.section_header("1", "¿QUE ES ESTE PROYECTO?")
    pdf.paragraph(
        "Es un proyecto de Mineria de Datos y Aprendizaje Automatico No Supervisado (Unsupervised Machine Learning). "
        "A diferencia del aprendizaje supervisado (donde los datos ya vienen con una etiqueta previa), en este proyecto tomamos "
        "947 objetos, armas, armaduras, monstruos y recursos de 'The Legend of Zelda' con 5 estadisticas numericas y dejamos que "
        "el algoritmo K-Means descubra de forma autonoma los patrones ocultos y grupos naturales (arquetipos de juego)."
    )

    # 2. PARA QUE SIRVE
    pdf.section_header("2", "¿PARA QUE SIRVE?")
    pdf.bullet("En la Industria de Videojuegos (Game Data Science)", "Sirve para auditar el balance y la curva de poder-costo de los objetos. Permite a los disenadores detectar armas sobrevaloradas o desbalances economicos en rupias frente a la proteccion.")
    pdf.bullet("Para el Jugador y Toma de Decisiones", "Permite planificar ranuras de inventario de forma optima: reservar armas de asalto para dano activo, escudos pesados para mitigacion pasiva y consumibles antes de enfrentar jefes colosales.")

    # 3. QUE CONTIENE EL PROYECTO
    pdf.section_header("3", "¿QUE CONTIENE EL PROYECTO?")
    pdf.bullet("Dataset Original (954 filas, 12 variables)", "Contiene imperfecciones controladas (7 duplicados exactos, valores nulos y anomalias negativas) para evidenciar el proceso de auditoria y limpieza.")
    pdf.bullet("Dataset Procesado (947 filas limpias)", "Normalizado, sin duplicados, con nulos imputados por mediana condicional y con las columnas 'Cluster', 'Cluster_Nombre', 'pca_x' y 'pca_y' integradas.")
    pdf.bullet("Codigo Fuente y Notebook", "Script reproducible 'src/analisis_kmeans.py' y Jupyter Notebook interactivo 'notebooks/proyecto_kmeans_zelda.ipynb' con todas las celdas ejecutadas y explicadas.")
    pdf.bullet("Dashboard Interactivo (Streamlit)", "Aplicacion web con diseno formal, sin emojis, con difuminados glassmorphism, 4 KPIs, 4 graficas analiticas interactivas, 3 filtros funcionales y 2 paginas independientes.")
    pdf.bullet("Reporte Oficial en PDF", "Informe de 8 paginas que cubre estrictamente los 8 apartados solicitados por la rubrica academica.")

    # 4. CONCEPTOS TEORICOS CLAVE
    pdf.section_header("4", "CONCEPTOS TEORICOS CLAVE QUE PREGUNTARA LA MAESTRA")
    
    pdf.paragraph(
        "K-Means es un algoritmo de agrupamiento particional. Selecciona K centroides iniciales (con k-means++), asigna cada punto al centroide "
        "mas cercano mediante Distancia Euclidiana, y recalcula iterativamente la posicion del centroide como el promedio (media) de sus puntos asignados hasta converger.",
        bold_prefix="Funcionamiento de K-Means:"
    )

    pdf.paragraph(
        "Las distancias euclidianas dependen de la escala numerica. En nuestro dataset el precio llega a 5,000 rupias y la durabilidad a 1,000, "
        "mientras que la rareza va de 1 a 5. Sin StandardScaler, la variable precio habria dominado el 99% de las agrupaciones. StandardScaler "
        "transforma todas las variables a media cero y varianza unitaria (Z-Score), otorgandoles el mismo peso geometrico.",
        bold_prefix="¿Por que fue obligatorio StandardScaler?"
    )

    pdf.paragraph(
        "Evaluamos 7 valores de K (de 2 a 8). En el Metodo del Codo (Inercia/SSE), K=4 marco el punto de inflexion de estabilizacion. "
        "El Coeficiente de Silueta en K=4 alcanzo 0.3959 (alta cohesion interna y adecuada separacion). Cualitativamente, K=4 refleja con exactitud "
        "los 4 roles del juego: dano ofensivo, blindaje defensivo, recoleccion y jefes colosales.",
        bold_prefix="¿Por que K=4 es la configuracion optima?"
    )

    pdf.paragraph(
        "Dado que entrenamos con 5 variables, no es posible graficar 5 dimensiones en un plano cartesiano. PCA aplico una transformacion ortogonal "
        "lineal para proyectar las 5 variables en 2 Componentes Principales, reteniendo el 70.8% de la varianza total de la informacion.",
        bold_prefix="¿Para que sirvio PCA (2D)?"
    )

    # 5. TABLA RESUMEN DE LOS 4 CLUSTERES
    pdf.add_page()
    pdf.section_header("5", "TABLA MAESTRA DE LOS 4 CLUSTERES DE HYRULE")
    
    # Encabezado tabla
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    
    cols = [50, 16, 16, 18, 22, 16, 36]
    pdf.cell(cols[0], 6, "Cluster Asignado", 1, 0, "C", True)
    pdf.cell(cols[1], 6, "Ataque", 1, 0, "C", True)
    pdf.cell(cols[2], 6, "Defensa", 1, 0, "C", True)
    pdf.cell(cols[3], 6, "Durabilidad", 1, 0, "C", True)
    pdf.cell(cols[4], 6, "Precio", 1, 0, "C", True)
    pdf.cell(cols[5], 6, "Cant.", 1, 0, "C", True)
    pdf.cell(cols[6], 6, "Composicion Tipica", 1, 1, "C", True)

    cluster_data = [
        ("Recursos Basicos y Consumibles", "8.1", "5.0", "33.1", "134 Rupias", "344 (36%)", "Setas, frutas, elixires, recetas"),
        ("Arsenal Ofensivo y Armas Asalto", "47.8", "0.7", "57.7", "571 Rupias", "432 (46%)", "Espadas, mandobles, sables, arcos"),
        ("Blindaje Tactico y Escudos", "1.1", "43.1", "104.7", "1,433 Rupias", "138 (15%)", "Escudos pesados, armaduras Hada"),
        ("Jefes Supremos y Calamidades", "75.7", "47.2", "706.2", "1,318 Rupias", "33 (3.5%)", "Ganon, Lynels Dorados/Plateados")
    ]
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(30, 41, 59)
    for c_nom, c_atk, c_def, c_dur, c_prc, c_cnt, c_comp in cluster_data:
        pdf.cell(cols[0], 5, f" {c_nom}", 1, 0, "L")
        pdf.cell(cols[1], 5, c_atk, 1, 0, "C")
        pdf.cell(cols[2], 5, c_def, 1, 0, "C")
        pdf.cell(cols[3], 5, c_dur, 1, 0, "C")
        pdf.cell(cols[4], 5, c_prc, 1, 0, "C")
        pdf.cell(cols[5], 5, c_cnt, 1, 0, "C")
        pdf.cell(cols[6], 5, f" {c_comp}", 1, 1, "L")

    pdf.ln(3)

    # 6. SIMULADOR DE PREGUNTAS Y RESPUESTAS DE LA MAESTRA
    pdf.section_header("6", "SIMULADOR DE PREGUNTAS Y RESPUESTAS RAPIDAS PARA EL EXAMEN")

    pdf.qa_card(
        "¿Por que eligieron un algoritmo no supervisado y no uno supervisado?",
        "Porque nuestro dataset no contaba con categorias predefinidas de exito o etiquetas previas. El objetivo era descubrir agrupaciones naturales basadas en la similitud geometrica de las variables de combate y economia."
    )

    pdf.qa_card(
        "¿Como trataron los valores nulos y duplicados?",
        "Eliminamos 7 duplicados exactos con drop_duplicates(). Para los nulos en precio y durabilidad, realizamos una imputacion contextual con la mediana por categoria (no la media global), evitando sesgos causados por objetos de valor extremo."
    )

    pdf.qa_card(
        "¿Que paso cuando compararon dos configuraciones de K (K=4 vs K=3)?",
        "Con K=3 la inercia fue mayor (2,503 vs 1,874) y la silueta cayo a 0.3553. Analiticamente, K=3 fusiono erroneamente el blindaje defensivo con las armas de ataque en un solo grupo mixto, perdiendo resolucion tactica. K=4 desacopla el rol protector del rol ofensivo."
    )

    pdf.qa_card(
        "¿Cuales son los 3 hallazgos principales que descubrieron?",
        "1. Polarizacion binaria: no existen armas hibridas (o hacen mucho dano o defienden mucho). 2. Asimetria de costo: las armaduras cuestan casi el triple que las armas (1,433 vs 571 Rupias). 3. Amenaza concentrada: los jefes (Cluster 3) tienen 12 veces mas vida util que el resto de las entidades."
    )

    pdf.qa_card(
        "¿Cuales son las limitaciones del modelo K-Means?",
        "K-Means presupone grupos hiper-esfericos y varianzas similares. Ademas, no toma en cuenta la ubicacion espacial ni los factores climaticos dinamicos del mapa de Hyrule."
    )

    # 7. DISCURSO DE PRESENTACION DE 1 MINUTO
    pdf.section_header("7", "DISCURSO DE PRESENTACION ORAL (SPEECH DE 1 MINUTO)")
    pdf.paragraph(
        "\"Buenos dias profesora y companeros. Nuestro proyecto integrador consistio en la mineria de datos y segmentacion no supervisada "
        "del compendio de 'The Legend of Zelda', analizando casi mil registros entre armas, armaduras, monstruos y recursos.\n"
        "Implementamos el algoritmo K-Means a partir de 5 dimensiones: ataque, defensa, durabilidad, precio y rareza. Tras la limpieza e imputacion "
        "de nulos, estandarizamos las variables con StandardScaler y evaluamos 7 valores de K mediante el metodo del codo y el coeficiente de silueta, "
        "determinando que K=4 es la configuracion optima.\n"
        "Esto nos permitio descubrir cuatro arquetipos claros: Armamento de Asalto, Blindaje Tactico, Recursos Basicos y Jefes de Calamidad.\n"
        "Finalmente, construimos un dashboard interactivo en Streamlit con KPIs y filtros multivariados para explorar los resultados en tiempo real, "
        "respaldado por nuestro informe formal en PDF y repositorio en GitHub.\""
    )

    # Guardar archivo
    output_path = "docs/Guia_Estudio_Defensa_Examen.pdf"
    os.makedirs("docs", exist_ok=True)
    pdf.output(output_path)
    print(f"Guía de estudio en PDF generada exitosamente en: {output_path}")
    print(f"Páginas totales: {pdf.page_no()}")

if __name__ == "__main__":
    build_pdf()
