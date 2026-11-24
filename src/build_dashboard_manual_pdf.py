"""
Script para generar el documento PDF oficial con las 10 capturas del dashboard
y sus fichas explicativas paso a paso para la defensa de clase:
docs/Manual_Explicativo_Dashboard_Capturas.pdf
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class DashboardManualPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=False) # Manejo manual de coordenadas para precisión milimétrica
        self.set_margins(left=14, top=14, right=14)

    def header(self):
        if self.page_no() > 1:
            self.set_xy(14, 8)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(100, 116, 139) # Slate 500
            self.cell(182, 5, "MANUAL EXPLICATIVO DEL DASHBOARD | HYRULE DATA INSIGHTS", border="B", align="L")

    def footer(self):
        self.set_xy(14, 287)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(182, 5, f"Pagina {self.page_no()} de {{nb}} | Proyecto Integrador Mineria de Datos K-Means", border="T", align="C")

    def page_title_banner(self, title, subtitle):
        self.set_xy(14, 14)
        self.set_fill_color(15, 23, 42) # Slate 900
        self.rect(14, 14, 182, 21, "F")
        self.set_fill_color(37, 99, 235) # Blue 600 line
        self.rect(14, 34, 182, 1.5, "F")
        
        self.set_xy(14, 17)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(248, 250, 252)
        self.cell(182, 6, title, align="C")
        self.set_xy(14, 25)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(148, 163, 184)
        self.cell(182, 5, subtitle, align="C")

    def draw_side_by_side_card(self, y_start, num_str, title_str, img_path, que_es, elementos, interpretacion, respuesta_examen):
        # Fondo y cabecera del bloque
        card_h = 116
        self.set_fill_color(248, 250, 252) # Slate 50
        self.set_draw_color(226, 232, 240) # Slate 200
        self.rect(14, y_start, 182, card_h, "DF")

        # Barra de título de la gráfica
        self.set_fill_color(241, 245, 249) # Slate 100
        self.rect(14, y_start, 182, 7, "F")
        self.set_fill_color(37, 99, 235) # Acento azul
        self.rect(14, y_start, 3, 7, "F")

        self.set_xy(19, y_start + 1)
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(15, 23, 42)
        self.cell(175, 5, f"Captura {num_str}: {title_str}", align="L")

        # Imagen a la izquierda (ancho 96mm)
        img_y = y_start + 9
        if os.path.exists(img_path):
            self.image(img_path, x=16, y=img_y, w=96)

        # Marco sutil para la imagen
        self.set_draw_color(203, 213, 225)
        self.rect(16, img_y, 96, 73, "D")

        # Texto a la derecha (ancho 80mm, x=114)
        t_x = 114
        t_w = 80
        curr_y = y_start + 9

        # ¿Qué es?
        self.set_xy(t_x, curr_y)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(30, 41, 59)
        self.cell(t_w, 4, "¿QUE ES ESTA GRAFICA?", align="L")
        curr_y += 4
        self.set_xy(t_x, curr_y)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(51, 65, 85)
        self.multi_cell(t_w, 3.4, que_es)
        curr_y = self.get_y() + 2

        # Elementos clave
        self.set_xy(t_x, curr_y)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(30, 41, 59)
        self.cell(t_w, 4, "ELEMENTOS VISUALES Y EJES:", align="L")
        curr_y += 4
        self.set_xy(t_x, curr_y)
        self.set_font("Helvetica", "", 7.3)
        self.set_text_color(51, 65, 85)
        self.multi_cell(t_w, 3.3, elementos)
        curr_y = self.get_y() + 2

        # Interpretación
        self.set_xy(t_x, curr_y)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(30, 41, 59)
        self.cell(t_w, 4, "INTERPRETACION ANALITICA:", align="L")
        curr_y += 4
        self.set_xy(t_x, curr_y)
        self.set_font("Helvetica", "", 7.3)
        self.set_text_color(51, 65, 85)
        self.multi_cell(t_w, 3.3, interpretacion)
        curr_y = self.get_y() + 2

        # Qué responderle a la maestra (destacado en caja ámbar/azul)
        self.set_fill_color(254, 243, 199) # Amber 100
        self.set_draw_color(245, 158, 11) # Amber 500
        box_h = y_start + card_h - curr_y - 2
        self.rect(t_x - 1, curr_y, t_w + 1, box_h, "DF")

        self.set_xy(t_x, curr_y + 1)
        self.set_font("Helvetica", "B", 7.6)
        self.set_text_color(180, 83, 9) # Amber 700
        self.cell(t_w, 3.5, "VOZ DEL EXAMEN (QUE RESPONDER):", align="L")
        self.set_xy(t_x, curr_y + 4.5)
        self.set_font("Helvetica", "I", 7.3)
        self.set_text_color(120, 53, 15)
        self.multi_cell(t_w, 3.2, f'"{respuesta_examen}"')


def generate_manual_pdf():
    pdf = DashboardManualPDF()
    pdf.alias_nb_pages()

    # =========================================================================
    # PÁGINA 1: CABECERA Y KPIS + BARRA LATERAL Y FILTROS
    # =========================================================================
    pdf.add_page()
    pdf.page_title_banner(
        "MANUAL EXPLICATIVO DEL DASHBOARD Y GUIA DE DEFENSA ORAL",
        "The Legend of Zelda: Hyrule Data Insights | Segmentacion Multivariada K-Means"
    )

    # 1. CABECERA EJECUTIVA Y KPIS
    y1 = 39
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(14, y1, 182, 86, "DF")

    pdf.set_fill_color(241, 245, 249)
    pdf.rect(14, y1, 182, 7, "F")
    pdf.set_fill_color(37, 99, 235)
    pdf.rect(14, y1, 3, 7, "F")

    pdf.set_xy(19, y1 + 1)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(175, 5, "Captura 1: Cabecera Ejecutiva y Tarjetas KPI en Tiempo Real", align="L")

    # Imagen cabecera
    img1 = "assets/capturas_dashboard/1_kpis_cabecera.jpg"
    if os.path.exists(img1):
        pdf.image(img1, x=16, y=y1 + 9, w=178)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(16, y1 + 9, 178, 34, "D")

    # Explicación de las 4 tarjetas
    kpi_y = y1 + 45
    col_w = 43.5
    kpis_data = [
        ("TOTAL OBSERVACIONES", "827 / 947", "Muestra activa tras aplicar los filtros de la barra lateral. Informa la representatividad muestral."),
        ("PODER OFENSIVO MEDIO", "31.5 pts", "Media aritmetica de impacto en combate de los items visibles en el catalogo."),
        ("DURABILIDAD MEDIANA", "40 pts", "Resistencia de vida util. Se usa la mediana y NO la media para neutralizar el sesgo de monstruos con 1,500 HP."),
        ("VALORACION PROMEDIO", "425 Rupias", "Costo economico promedio en rupias dentro del ecosistema comercial de Hyrule.")
    ]
    for i, (k_title, k_val, k_desc) in enumerate(kpis_data):
        cx = 16 + i * (col_w + 1.2)
        pdf.set_fill_color(255, 255, 255)
        pdf.rect(cx, kpi_y, col_w, 28, "DF")
        pdf.set_xy(cx + 1, kpi_y + 1.5)
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(col_w - 2, 3.5, k_title, align="C")
        pdf.set_xy(cx + 1, kpi_y + 6)
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(col_w - 2, 5, k_val, align="C")
        pdf.set_xy(cx + 1.5, kpi_y + 12)
        pdf.set_font("Helvetica", "", 6.7)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(col_w - 3, 2.9, k_desc, align="C")

    # Voz de examen para KPIs
    pdf.set_fill_color(254, 243, 199)
    pdf.set_draw_color(245, 158, 11)
    pdf.rect(16, y1 + 75, 178, 9, "DF")
    pdf.set_xy(18, y1 + 76)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(180, 83, 9)
    pdf.cell(42, 3.5, "Voz del Examen (KPIs):", align="L")
    pdf.set_font("Helvetica", "I", 7.2)
    pdf.set_text_color(120, 53, 15)
    pdf.write(3.5, '"La cabecera actualiza dinamicamente el pulso del catalogo. Usamos la mediana en durabilidad (40 pts) para evitar distorsiones por valores atipicos extremos de monstruos colosales."')

    # 2. BARRA LATERAL Y FILTROS MULTIVARIADOS
    y2 = 128
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(14, y2, 182, 154, "DF")

    pdf.set_fill_color(241, 245, 249)
    pdf.rect(14, y2, 182, 7, "F")
    pdf.set_fill_color(37, 99, 235)
    pdf.rect(14, y2, 3, 7, "F")

    pdf.set_xy(19, y2 + 1)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(175, 5, "Captura 2: Panel de Control y Filtros Multivariados de Seleccion", align="L")

    # Imagen lateral vertical (379x1024 -> w=50mm, h=135mm)
    img6 = "assets/capturas_dashboard/6_barra_lateral_filtros.png"
    if os.path.exists(img6):
        pdf.image(img6, x=16, y=y2 + 9, w=50)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(16, y2 + 9, 50, 135, "D")

    # Texto a la derecha
    r_x = 70
    r_w = 123
    r_y = y2 + 9

    pdf.set_xy(r_x, r_y)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(r_w, 4.5, "¿QUE ES Y QUE FUNCION CUMPLE ESTE PANEL?", align="L")
    r_y += 5
    pdf.set_xy(r_x, r_y)
    pdf.set_font("Helvetica", "", 7.8)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(r_w, 3.6, 
        "Es el centro de mando interactivo del dashboard implementado mediante 'st.sidebar'. "
        "Permite segmentar y aislar subconjuntos de datos en tiempo real mediante 4 componentes de filtrado combinados "
        "con logica booleana AND, superando ampliamente el requerimiento de 3 filtros solicitado en la rubrica."
    )
    r_y = pdf.get_y() + 3

    filtros_det = [
        ("Navegacion (Radio Button)", "Permite conmutar instantaneamente entre la Pagina 1 ('Analisis General') y la Pagina 2 ('Segmentacion K-Means') sin recargar la aplicacion."),
        ("Filtro por Cluster (Multiselect)", "Permite aislar o combinar los 4 grupos descubiertos por K-Means (Arsenal Ofensivo, Blindaje Tactico, Jefes Supremos, Recursos Basicos)."),
        ("Filtro por Categoria (Multiselect)", "Segmenta el catalogo por arquetipo de objeto: Bows (Arcos), Weapons (Armas), Shields (Escudos), Materials, Monsters y Consumables."),
        ("Slider de Precio (Rango Continuo)", "Filtra por valor de venta en el mercado de Hyrule desde 0 hasta 6,770 Rupias."),
        ("Slider de Rareza (Tier 1 a 5)", "Segmenta por jerarquia de exclusividad del objeto desde comunes (Tier 1) hasta tesoros legendarios (Tier 5).")
    ]

    for f_nom, f_desc in filtros_det:
        pdf.set_xy(r_x, r_y)
        pdf.set_font("Helvetica", "B", 7.8)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(4, 3.8, "-")
        pdf.set_font("Helvetica", "B", 7.8)
        pdf.cell(52, 3.8, f"{f_nom}:")
        pdf.set_font("Helvetica", "", 7.4)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(r_w - 56, 3.5, f_desc)
        r_y = pdf.get_y() + 1.5

    # Caja de voz del examen
    r_y += 2
    pdf.set_fill_color(254, 243, 199)
    pdf.set_draw_color(245, 158, 11)
    pdf.rect(r_x, r_y, r_w, 24, "DF")
    pdf.set_xy(r_x + 2, r_y + 1.5)
    pdf.set_font("Helvetica", "B", 7.8)
    pdf.set_text_color(180, 83, 9)
    pdf.cell(r_w - 4, 3.5, "VOZ DEL EXAMEN (DEFENSA ANTE LA PROFESORA):", align="L")
    pdf.set_xy(r_x + 2, r_y + 5.5)
    pdf.set_font("Helvetica", "I", 7.4)
    pdf.set_text_color(120, 53, 15)
    pdf.multi_cell(r_w - 4, 3.4, 
        '"El panel lateral implementa navegacion multipagina y filtros multivariados interactivos. '
        'Al mover un slider o deseleccionar una categoria, el dataframe se recalcula en memoria y todas las graficas '
        'y KPIs se sincronizan de inmediato para permitir analisis granulares y drill-down."'
    )

    # =========================================================================
    # PÁGINA 2: ANÁLISIS GENERAL (DISPERSIÓN DURABILIDAD VS PRECIO + HISTOGRAMA ATAQUE)
    # =========================================================================
    pdf.add_page()

    # 3. DISPERSIÓN DURABILIDAD VS PRECIO
    pdf.draw_side_by_side_card(
        y_start=18,
        num_str="3",
        title_str="Relacion entre Durabilidad y Precio de Venta",
        img_path="assets/capturas_dashboard/2_dispersion_durabilidad_precio.jpg",
        que_es="Grafico de dispersion multivariado (Scatter Plot) con burbujas ponderadas por rareza (Tier 1 a 5) y coloreadas por categoria de item.",
        elementos=(
            "Eje X: Durabilidad / Puntos de vida (0 a 1,500 HP).\n"
            "Eje Y: Precio de venta comercial (0 a 7,000 Rupias).\n"
            "Colores: Weapons (azul), Bows (rojo), Shields (verde), Materials (morado), Monsters (naranja).\n"
            "Tamano de burbuja: Nivel de rareza del objeto."
        ),
        interpretacion=(
            "- Arriba a la derecha: Arcos legendarios (rojo) y Escudos Hylianos (verde) alcanzan precios maximos (4,000 a 6,800 rupias) con durabilidad alta.\n"
            "- Abajo a la derecha: Monstruos (naranja) poseen hasta 1,400 de vida pero precio nulo (entidades salvajes no transables).\n"
            "- Abajo izquierda: Concentracion masiva de items comunes (<200 HP y <2,000 rupias)."
        ),
        respuesta_examen="Demuestra visualmente la asimetria economica: el valor mercantil no depende de la durabilidad bruta, sino de si el item es equipo artificial exclusivo o una criatura hostil de campo."
    )

    # 4. HISTOGRAMA DAÑO OFENSIVO
    pdf.draw_side_by_side_card(
        y_start=138,
        num_str="4",
        title_str="Distribucion de Dano Ofensivo por Categoria",
        img_path="assets/capturas_dashboard/3_histograma_ataque.jpg",
        que_es="Histograma de frecuencias apiladas que clasifica el dano destructivo de todo el catalogo desglosado por categoria.",
        elementos=(
            "Eje X: Poder de Ataque en Puntos (intervalos de 0 a 170 pts).\n"
            "Eje Y: Frecuencia / Conteo de items (count de 0 a 140).\n"
            "Capas apiladas: Morado (Materiales), Cian (Consumibles), Azul (Armas), Rojo (Arcos), Naranja (Monstruos)."
        ),
        interpretacion=(
            "- Pico masivo en 0 pts (>130 items): Recursos de crafteo, forraje y comida sin capacidad de ataque directo.\n"
            "- Campana principal de combate (20 a 80 pts): Armamento regular de espadas, mandobles y arcos.\n"
            "- Cola extendida a la derecha (>100 pts): Fusiones de elite y materiales de jefes con poder letal colosal."
        ),
        respuesta_examen="Evidencia la bimodalidad del catalogo: una poblacion masiva pasiva en cero dano (soporte) y una distribucion combativa sesgada a la derecha con media de 47.8 puntos en armas regulares."
    )

    # =========================================================================
    # PÁGINA 3: ANÁLISIS GENERAL (BARRAS GEOGRÁFICAS + MATRIZ DE CORRELACIÓN)
    # =========================================================================
    pdf.add_page()

    # 5. BARRAS GEOGRÁFICAS
    pdf.draw_side_by_side_card(
        y_start=18,
        num_str="5",
        title_str="Distribucion Geografica de Items por Region",
        img_path="assets/capturas_dashboard/4_barras_region.jpg",
        que_es="Grafico de barras horizontales ordenado de mayor a menor con escala de degradado formal en tonos de azul.",
        elementos=(
            "Eje Y: Regiones geograficas del reino de Hyrule.\n"
            "Eje X: Cantidad de registros / items descubiertos (0 a 160).\n"
            "Color: Degradado desde azul marino profundo (zonas mas densas) hasta celeste claro (zonas exclusivas)."
        ),
        interpretacion=(
            "- Depths (Subsuelo) lidera con mas de 155 items: es la region de mayor exploracion y botin de forja.\n"
            "- Central Hyrule (~133) y Death Mountain (~125) son los principales nucleos de combate y minerales.\n"
            "- Zonas de elite (Hyrule Castle con ~60 registros) tienen menos objetos pero concentran el armamento de mayor tier."
        ),
        respuesta_examen="Demuestra el balance ecologico y de diseno de niveles del mapa abierto: la densidad de objetos disminuye conforme aumenta el peligro o la exclusividad de la region."
    )

    # 6. MATRIZ DE CORRELACIÓN
    pdf.draw_side_by_side_card(
        y_start=138,
        num_str="6",
        title_str="Matriz de Correlacion Numerica Multivariada (Heatmap)",
        img_path="assets/capturas_dashboard/5_matriz_correlacion.jpg",
        que_es="Mapa de calor (Heatmap 5x5) con coeficientes de correlacion lineal de Pearson (r entre -1.0 y +1.0) entre las variables analizadas.",
        elementos=(
            "Variables: attack, defense, durability, sell_price, rarity.\n"
            "Escala de color: Paleta divergente formal con valores numericos etiquetados en cada celda.\n"
            "Diagonal principal: Identidad r = 1.00."
        ),
        interpretacion=(
            "- attack vs defense = -0.08: Correlacion nula/ortogonal (los items atacan o defienden, no hay hibridos).\n"
            "- attack vs rarity = +0.51: Fuerte asociacion positiva (a mayor rareza, mayor capacidad destructiva).\n"
            "- defense vs durability = +0.49: Los escudos y armaduras poseen la mayor resistencia al desgaste.\n"
            "- attack vs durability = +0.12: Baja relacion (las armas filosas se rompen rapido)."
        ),
        respuesta_examen="Es la prueba matematica que justifica el uso de K-Means: dado que ataque y defensa tienen correlacion de -0.08, el clustering particional separa de forma limpia y natural los roles de asalto de los roles protectores."
    )

    # =========================================================================
    # PÁGINA 4: SEGMENTACIÓN K-MEANS (DONA + PROYECCIÓN PCA 2D)
    # =========================================================================
    pdf.add_page()

    # 7. DONA PROPORCIÓN POR CLÚSTER
    pdf.draw_side_by_side_card(
        y_start=18,
        num_str="7",
        title_str="Grafico de Dona: Proporcion de Registros por Cluster",
        img_path="assets/capturas_dashboard/7_dona_proporcion_cluster.jpg",
        que_es="Grafico circular de anillo (Donut Chart) que expone el peso porcentual de cada uno de los 4 conglomerados descubiertos por K-Means.",
        elementos=(
            "Sector Rojo (52.2%): Arsenal Ofensivo y Armas de Asalto.\n"
            "Sector Verde (39.4%): Recursos Basicos, Forraje y Consumibles.\n"
            "Sector Azul (4.35%): Blindaje Tactico, Armaduras y Escudos.\n"
            "Sector Naranja (3.99%): Jefes Supremos, Calamidades y Reliquias Míticas."
        ),
        interpretacion=(
            "- El 91.6% del universo de Hyrule esta dominado por la interaccion basica: atacar (52.2%) y recolectar (39.4%).\n"
            "- Los escudos y blindaje representan un nicho defensivo muy selecto (4.35%).\n"
            "- Los jefes y calamidades forman una elite aislada del 3.99% (33 entidades supremas)."
        ),
        respuesta_examen="Comprueba que la distribucion de clusters refleja una estructura piramidal coherente de juego de rol: una base masiva de combate y forraje, coronada por minorias exclusivas de blindaje pesado y jefes colosales."
    )

    # 8. PROYECCIÓN PCA 2D
    pdf.draw_side_by_side_card(
        y_start=138,
        num_str="8",
        title_str="Proyeccion de Clusteres en PCA 2D (70.8% Varianza Explicada)",
        img_path="assets/capturas_dashboard/8_pca_2d_clusteres.jpg",
        que_es="Visualizacion bidimensional de las 5 dimensiones originales reducidas mediante Analisis de Componentes Principales (PCA).",
        elementos=(
            "Eje X: Componente Principal 1 - PC1 (44.7% varianza, carga en Dano Ofensivo y Rareza).\n"
            "Eje Y: Componente Principal 2 - PC2 (26.1% varianza, carga en Blindaje y Precio).\n"
            "Varianza total acumulada retenida: 70.8%.\n"
            "Colores: Asignacion por cluster (Rojo, Verde, Azul, Naranja)."
        ),
        interpretacion=(
            "- Verde (Recursos): Agrupado en cuadrante negativo (-2 a 0), sin ataque ni defensa.\n"
            "- Rojo (Arsenal): Diagonal ascendente hacia arriba a la derecha (ataque moderado-alto).\n"
            "- Azul (Blindaje): Proyectado fuertemente hacia abajo (alto blindaje, ataque nulo).\n"
            "- Naranja (Jefes): Totalmente aislados a la extrema derecha (PC1 entre 3 y 8)."
        ),
        respuesta_examen="Valida geometricamente la calidad del modelo K-Means: las fronteras entre clusters son nitidas y demuestran que los Jefes Supremos son entidades matematicamente singulares que se separan del resto del universo."
    )

    # =========================================================================
    # PÁGINA 5: GRÁFICAS ADICIONALES (BOXPLOT ATAQUE + ATAQUE VS PRECIO)
    # =========================================================================
    pdf.add_page()

    # 9. BOXPLOT ATAQUE POR CLÚSTER
    pdf.draw_side_by_side_card(
        y_start=18,
        num_str="9",
        title_str="Grafica Adicional 1: Dispersion del Poder Ofensivo (Boxplot)",
        img_path="assets/capturas_dashboard/9_boxplot_ataque_clusters.jpg",
        que_es="Diagrama de cajas y bigotes (Boxplot) que compara la dispersion estadistica, cuartiles y valores atipicos del dano entre los 4 clusters.",
        elementos=(
            "Eje X: Los 4 clusters de K-Means.\n"
            "Eje Y: Poder de Ataque en Puntos (0 a 150 pts).\n"
            "Cajas: Q1 (percentil 25), Linea central (Mediana/Q2), Q3 (percentil 75), Bigotes (1.5 * IQR) y Puntos (Outliers)."
        ),
        interpretacion=(
            "- Caja Roja (Arsenal): Mediana de 48 pts, IQR de 35 a 68 pts, con outliers que alcanzan 130 pts (armas fusionadas).\n"
            "- Caja Verde (Recursos) y Azul (Blindaje): Mediana 0 pts (carecen de poder ofensivo directo).\n"
            "- Caja Naranja (Jefes): La mas elevada de todas, mediana de 75 pts y rango que llega hasta 135 pts."
        ),
        respuesta_examen="Cumple el requisito de graficas comparativas adicionales. Demuestra cuantitativamente que el Cluster 3 (Jefes) es el mas letal de Hyrule, mientras que el Cluster 1 (Arsenal) concentra la fuerza de combate del jugador."
    )

    # 10. DISPERSIÓN ATAQUE VS PRECIO
    pdf.draw_side_by_side_card(
        y_start=138,
        num_str="10",
        title_str="Grafica Adicional 2: Relacion Ataque vs Precio en Rupias",
        img_path="assets/capturas_dashboard/10_dispersion_ataque_precio_clusters.jpg",
        que_es="Diagrama de dispersion que cruza la capacidad de dano destructivo contra el valor economico en rupias, segmentado por cluster.",
        elementos=(
            "Eje X: Poder de Ataque (0 a 160 pts).\n"
            "Eje Y: Precio en Rupias (0 a 7,000 Rupias).\n"
            "Colores: Rojo (Arsenal), Verde (Recursos), Azul (Blindaje), Naranja (Jefes y Reliquias)."
        ),
        interpretacion=(
            "- Columna azul en ataque=0: Escudos costosos de alta proteccion que alcanzan hasta 2,000 rupias sin infligir dano.\n"
            "- Franja roja horizontal (20 a 120 pts, <2,200 rupias): Armas regulares de reposicion continua con costo comercial asequible.\n"
            "- Puntos naranjas superiores (5,000 a 6,800 rupias): Reliquias y arcos sagrados de valor incalculable.\n"
            "- Puntos naranjas en Y=0: Partes de monstruos que no se compran en bazares."
        ),
        respuesta_examen="Evidencia la logica de equilibrio mercantil del videojuego: las armas de uso continuo se mantienen baratas para no frustrar la reposicion por rotura, mientras que la armadura pesada y las reliquias tienen precios prohibitivos."
    )

    # =========================================================================
    # PÁGINA 6: MATRIZ DE DEFENSA Y PREGUNTAS TRAMPA DE LA MAESTRA
    # =========================================================================
    pdf.add_page()
    pdf.page_title_banner(
        "MATRIZ MAESTRA DE DEFENSA ORAL ANTE LA PROFESORA",
        "Respuestas Tecnicas Concisa a las Preguntas Clave del Examen de Evaluacion"
    )

    y_qa = 39
    qa_list = [
        (
            "1. ¿Por que eligieron un algoritmo No Supervisado (K-Means) y no uno Supervisado?",
            "Porque nuestro compendio de datos no contaba con etiquetas previas ni clasificaciones de exito comerciales. El objetivo de la mineria era descubrir autonomamente las agrupaciones naturales y arquetipos de diseno ocultos a partir de la similitud geometrica de las estadisticas."
        ),
        (
            "2. ¿Por que fue estrictamente obligatorio usar StandardScaler antes de K-Means?",
            "K-Means calcula distancias euclidianas. En nuestro dataset, el precio llega a 6,770 rupias y la durabilidad a 1,500, mientras que la rareza va de 1 a 5. Sin estandarizacion, la variable precio habria dominado el 99% de las distancias. StandardScaler normaliza todas las variables a media 0 y varianza 1."
        ),
        (
            "3. ¿Como justificaron matematicamente la eleccion de K=4?",
            "Evaluamos 7 valores de K (2 a 8). En el Metodo del Codo (Inercia), K=4 marco el punto de inflexion (1,874.44). El Coeficiente de Silueta alcanzo un solido 0.3959. Analiticamente, K=3 fusionaba erroneamente armas y escudos en un grupo mixto, perdiendo resolucion tactica. K=4 es la separacion optima."
        ),
        (
            "4. ¿Que hicieron con los datos sucios (nulos, duplicados y negativos)?",
            "Eliminamos 7 filas duplicadas exactas. Para los valores negativos causados por errores de captura en precio, aplicamos valor absoluto. Para los valores nulos, realizamos una imputacion contextual con la mediana por categoria (no la media global), evitando sesgos por objetos de precio extremo."
        ),
        (
            "5. ¿Para que sirvio PCA (Analisis de Componentes Principales)?",
            "Entrenamos el modelo con 5 variables numericas, lo que hace imposible graficarlo en un plano cartesiano. PCA aplico una transformacion ortogonal lineal para sintetizar las 5 variables en 2 Componentes Principales (PC1 y PC2), reteniendo el 70.8% de la varianza total de la informacion."
        ),
        (
            "6. ¿Cuales son los 3 hallazgos de negocio/diseno mas relevantes del proyecto?",
            "1. Polarizacion radical: Ataque y defensa son ortogonales (r = -0.08); no existen objetos hibridos. 2. Asimetria de mercado: El blindaje defensivo es 2.5 veces mas costoso que el armamento ofensivo (1,433 vs 571 rupias). 3. Amenaza concentrada: Los jefes representan el 3.99% pero tienen 12 veces mas durabilidad."
        ),
        (
            "7. Speech de 45 segundos para abrir la presentacion del proyecto:",
            "\"Buenos dias profesora. Nuestro proyecto es una auditoria de mineria de datos no supervisada sobre el compendio de The Legend of Zelda, analizando 947 registros en 5 dimensiones de combate y economia. Tras auditar duplicados y valores atipicos, estandarizamos con StandardScaler y determinamos mediante el Metodo del Codo y Silueta que K=4 es la configuracion optima. Descubrimos cuatro arquetipos: Arsenal Ofensivo (52%), Recursos Basicos (39%), Blindaje Tactico (4.4%) y Jefes Supremos (4.0%). Todo el analisis fue sintetizado en un dashboard interactivo en Streamlit con KPIs y filtros multivariados en tiempo real.\""
        )
    ]

    for q, a in qa_list:
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(226, 232, 240)
        
        is_speech = "Speech" in q
        h_box = 36 if is_speech else 28
        
        if is_speech:
            pdf.set_fill_color(238, 242, 255) # Indigo 50
            pdf.set_draw_color(199, 210, 254)

        pdf.rect(14, y_qa, 182, h_box, "DF")

        pdf.set_xy(17, y_qa + 1.5)
        pdf.set_font("Helvetica", "B", 8.3)
        pdf.set_text_color(180, 83, 9 if not is_speech else 67) # Amber / Indigo
        if is_speech:
            pdf.set_text_color(67, 56, 202)
        pdf.cell(176, 4, q, align="L")

        pdf.set_xy(17, y_qa + 6)
        pdf.set_font("Helvetica", "I" if is_speech else "", 7.6)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(176, 3.4, a)

        y_qa += h_box + 2.5

    # Guardar documento
    output_path = "docs/Manual_Explicativo_Dashboard_Capturas.pdf"
    os.makedirs("docs", exist_ok=True)
    pdf.output(output_path)
    print(f"Manual de capturas en PDF generado exitosamente en: {output_path}")
    print(f"Páginas totales generadas: {pdf.page_no()}")

if __name__ == "__main__":
    generate_manual_pdf()
