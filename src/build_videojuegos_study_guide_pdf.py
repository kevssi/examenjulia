"""
Script para compilar la Guía de Estudio y Defensa en PDF sobre Ventas de Videojuegos Físicos vs Digitales:
docs/Guia_Estudio_Defensa_Examen.pdf
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class StudyGuidePDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=18, top=16, right=18)

    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 6, "GUIA DE ESTUDIO Y DEFENSA ORAL | MINERIA DE DATOS K-MEANS: VENTAS DE VIDEOJUEGOS", border="B", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)

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
        self.set_font("Helvetica", "B", 12.5)
        self.set_text_color(248, 250, 252)
        self.cell(0, 6, title, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(148, 163, 184)
        self.cell(0, 5, subtitle, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def section_header(self, num_str, title_str):
        self.ln(2)
        self.set_fill_color(241, 245, 249)
        self.set_draw_color(203, 213, 225)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(15, 23, 42)
        self.cell(0, 7, f"  {num_str}. {title_str}", fill=True, border="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def paragraph(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(51, 65, 85)
        if bold_prefix:
            self.set_font("Helvetica", "B", 8.5)
            self.write(4.2, bold_prefix + " ")
            self.set_font("Helvetica", "", 8.5)
        self.write(4.2, text + "\n\n")

    def bullet(self, title, desc):
        self.set_font("Helvetica", "B", 8.3)
        self.set_text_color(30, 41, 59)
        self.cell(4, 4.2, "-", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(42, 4.2, f"{title}: ", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_font("Helvetica", "", 8.3)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.2, desc)
        self.ln(1)

    def qa_card(self, question, answer):
        self.set_fill_color(248, 250, 252)
        self.set_draw_color(226, 232, 240)
        
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(180, 83, 9) # Amber 700
        self.cell(0, 5, f"Pregunta: {question}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_font("Helvetica", "", 8.3)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4, f"Respuesta: {answer}")
        self.ln(2)

def build_videojuegos_study_guide():
    pdf = StudyGuidePDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Banner
    pdf.card_banner(
        "GUIA DE ESTUDIO: SEGMENTACION DE VENTAS DE VIDEOJUEGOS",
        "Mineria de Datos K-Means | Rendimiento Comercial Fisico vs. Digital"
    )

    # 1. PROBLEMATICA
    pdf.section_header("1", "¿CUAL ES LA PROBLEMATICA QUE SE ESTA ANALIZANDO?")
    pdf.paragraph(
        "\"La problematica central es el riesgo de perdida economica e inventario estancado en tiendas y distribuidoras "
        "de videojuegos, provocado por la falta de certeza sobre que titulos venden mas, cuales venden menos y en que "
        "formato (fisico o digital) rinde mejor cada uno.\"",
        bold_prefix="Definicion Clara y Directa:"
    )
    pdf.bullet("Perdidas por Discos Físicos en Almacen", "Fabricar discos y transportarlos a tiendas cuesta millones. Si la tienda compra miles de unidades de un juego impopular, el producto se queda acumulando polvo en almacenes como inventario muerto.")
    pdf.bullet("Desaprovechamiento del Canal Digital", "Hay juegos (como indies y shooters multijugador) que casi no se compran en caja fisica pero generan millones en descargas digitales. Producir cajas fisicas para ellos es un desperdicio de dinero.")
    pdf.bullet("Decisiones a Ciegas", "Existen casi 1,000 videojuegos lanzados cada ano. Sin mineria de datos, los directores comerciales tendrian que adivinar que titulos reabastecer y cuales liquidar con descuento.")

    # 2. PARA QUE SIRVE
    pdf.section_header("2", "¿PARA QUE SIRVE Y QUE SOLUCIONA?")
    pdf.bullet("Optimizacion de Inventario y Cadena de Suministro", "Permite a las distribuidoras saber exactamente cuanto stock fisico pedir a fabrica y evitar sobrecostos de almacenamiento.")
    pdf.bullet("Estrategia de Lanzamiento Comercial", "Permite decidir si un juego debe lanzarse exclusivamente en formato digital (ahorrando cajas y envios) o si vale la pena imprimir una edicion fisica de coleccion.")
    pdf.bullet("Identificacion Temprana de Fracasos", "Detecta de inmediato los juegos de bajo rendimiento para aplicar promociones rapidas antes de que su valor comercial caiga a cero.")

    # 3. QUE CONTIENE EL PROYECTO
    pdf.section_header("3", "¿QUE CONTIENE EL PROYECTO?")
    pdf.bullet("Dataset Original (928 filas, 12 columnas)", "Contiene datos reales de mercado con anomalias controladas (duplicados, valores nulos y valores negativos) para evidenciar la etapa de auditoria y limpieza.")
    pdf.bullet("Dataset Procesado (920 filas limpias)", "Normalizado con StandardScaler, nulos imputados por mediana contextual segun genero, y con los clusters descubiertos y coordenadas PCA integradas.")
    pdf.bullet("Modelo No Supervisado K-Means (K=4)", "Validado mediante el Metodo del Codo (Inercia = 1,415.33), Coeficiente de Silueta (0.4197), Calinski-Harabasz (687.04) y PCA 2D (75.2% varianza retenida).")
    pdf.bullet("Dashboard Interactivo Streamlit", "Aplicacion analitica profesional con 4 KPIs en tiempo real, 4 graficas multivariadas interactivas, 5 filtros combinables y explorador de datos.")

    # 4. TABLA DE LOS 4 CLUSTERES
    pdf.add_page()
    pdf.section_header("4", "LOS 4 CLUSTERES DESCUBIERTOS POR K-MEANS")
    
    # Tabla
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    
    cols = [48, 22, 22, 22, 20, 40]
    pdf.cell(cols[0], 6, "Cluster Asignado", 1, 0, "C", True)
    pdf.cell(cols[1], 6, "Venta Fisica", 1, 0, "C", True)
    pdf.cell(cols[2], 6, "Venta Digital", 1, 0, "C", True)
    pdf.cell(cols[3], 6, "Calif. Media", 1, 0, "C", True)
    pdf.cell(cols[4], 6, "Proporcion", 1, 0, "C", True)
    pdf.cell(cols[5], 6, "Estrategia de Negocio", 1, 1, "C", True)

    cluster_table = [
        ("Superventas Globales (Blockbusters)", "8.69 M copias", "12.00 M copias", "88 pts", "169 (18.4%)", "Prioridad maxima de stock y campanas publicitarias."),
        ("Éxitos Digitales e Indies Virales", "0.60 M copias", "7.80 M copias", "82 pts", "317 (34.5%)", "Vender exclusivamente en digital; cero gasto en cajas."),
        ("Coleccionables de Consola (Físico Fuerte)", "6.65 M copias", "2.50 M copias", "84 pts", "210 (22.8%)", "Fabricar ediciones especiales en caja para fans."),
        ("Fracasos Comerciales y Bajo Rendimiento", "0.41 M copias", "0.50 M copias", "54 pts", "224 (24.3%)", "Liquidar con descuentos; no pedir mas inventario.")
    ]
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(30, 41, 59)
    for c_nom, c_fis, c_dig, c_cal, c_pct, c_est in cluster_table:
        pdf.cell(cols[0], 5.5, f" {c_nom}", 1, 0, "L")
        pdf.cell(cols[1], 5.5, c_fis, 1, 0, "C")
        pdf.cell(cols[2], 5.5, c_dig, 1, 0, "C")
        pdf.cell(cols[3], 5.5, c_cal, 1, 0, "C")
        pdf.cell(cols[4], 5.5, c_pct, 1, 0, "C")
        pdf.cell(cols[5], 5.5, f" {c_est}", 1, 1, "L")

    pdf.ln(3)

    # 5. PREGUNTAS TRAMPA
    pdf.section_header("5", "SIMULADOR DE PREGUNTAS Y RESPUESTAS PARA EL EXAMEN")

    pdf.qa_card(
        "¿Por que usaron K-Means (No Supervisado) y no un modelo de clasificacion (Supervisado)?",
        "Porque no teniamos una columna previa que dijera 'juego exitoso' o 'juego fracasado'. El objetivo era que el algoritmo descubriera de forma autonoma las agrupaciones naturales basadas en las ventas fisicas y digitales sin ningun sesgo humano."
    )

    pdf.qa_card(
        "¿Por que fue indispensable usar StandardScaler?",
        "Porque las variables tenian escalas muy desiguales: la calificacion va de 0 a 100, el precio de 20 a 70 dolares, y las ventas van de 0 a 15 millones. Sin StandardScaler, la calificacion y el precio habrian dominado el 90% del calculo de distancias euclidianas."
    )

    pdf.qa_card(
        "¿Como determinaron que K=4 era el numero optimo de grupos?",
        "Evaluamos K de 2 a 8. En K=4 se produjo el punto de codo de estabilizacion de la inercia (1,415.3) y el Coeficiente de Silueta alcanzo su valor mas alto y solido (0.4197). Ademas, K=4 coincide con los 4 perfiles reales del mercado de videojuegos."
    )

    pdf.qa_card(
        "¿Que hallazgo principal de negocio descubrieron?",
        "Descubrimos que casi el 35% del catalogo pertenece al cluster de 'Exitos Digitales', donde la venta digital supera por mas de 10 a 1 a la venta fisica. Esto demuestra que imprimir discos fisicos para ese segmento representa una perdida financiera directa para la distribuidora."
    )

    # 6. DISCURSO DE PRESENTACIÓN DE 45 SEGUNDOS
    pdf.section_header("6", "SPEECH DE PRESENTACION ORAL (LO QUE DEBES DECIR AL INICIAR)")
    pdf.paragraph(
        "\"Buenos dias profesora. Nuestro proyecto es una investigacion de mineria de datos no supervisada orientada a la industria "
        "del entretenimiento interactivo. La problematica principal es el riesgo financiero e inventario muerto que sufren las tiendas "
        "de videojuegos al no tener certeza sobre que juegos venden mas, cuales venden menos y en que canal (fisico o digital) se desempenan mejor.\n"
        "Analizamos mas de 900 videojuegos mediante el algoritmo K-Means. Tras limpiar y estandarizar las variables, validamos que K=4 es la configuracion "
        "optima, descubriendo cuatro arquetipos claros: Superventas Blockbusters (18%), Exitos Digitales (35%), Coleccionables Fisicos (23%) y Fracasos Comerciales (24%).\n"
        "Finalmente, construimos un dashboard interactivo en Streamlit con KPIs y filtros en tiempo real para apoyar la toma de decisiones comerciales.\""
    )

    output_path = "docs/Guia_Estudio_Defensa_Examen.pdf"
    os.makedirs("docs", exist_ok=True)
    pdf.output(output_path)
    print(f"Guía de estudio en PDF generada exitosamente en: {output_path}")

if __name__ == "__main__":
    build_videojuegos_study_guide()
