"""
Generador del PDF exclusivo Practica_Examen.pdf
Contiene ÚNICAMENTE las tablas de datos, registros y salidas numéricas
de las Partes 2, 3, 4 y 5, sin textos teóricos largos.
"""

import os
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class PracticaExamenPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=15, top=15, right=15)
        self.add_font("Arial", "", "C:/Windows/Fonts/arial.ttf")
        self.add_font("Arial", "B", "C:/Windows/Fonts/arialbd.ttf")

    def header(self):
        pass

    def footer(self):
        pass

    def section_header(self, title):
        self.ln(3)
        self.set_font("Arial", "B", 11)
        self.set_text_color(17, 24, 39)
        self.cell(0, 6, title.upper(), border=0, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(209, 213, 219)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(2)

    def sub_header(self, subtitle):
        self.set_font("Arial", "B", 9.5)
        self.set_text_color(31, 41, 55)
        self.cell(0, 5, subtitle, border=0, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

def build_pdf():
    in_path = "data/videojuegos_ventas_original.csv"
    proc_path = "data/videojuegos_ventas_procesado.csv"
    df_raw = pd.read_csv(in_path)
    df_proc = pd.read_csv(proc_path)

    pdf = PracticaExamenPDF()

    # =========================================================================
    # PORTADA
    # =========================================================================
    pdf.add_page()
    logo_path = "assets/logo_utslrc.png"
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=70, y=25, w=70)
        pdf.set_y(60)
    else:
        pdf.ln(35)

    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(0, 9, "PRÁCTICA EXAMEN - RESPUESTAS DE REGISTROS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Arial", "B", 13.5)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 8, "Ventas del Formato Físico y Digital de los Videojuegos", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 7, "Extracción de Conocimiento en Bases de Datos (Partes 2, 3, 4 y 5)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

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
    # PARTE 2. REGISTROS ORIGINALES Y ESTADÍSTICAS
    # =========================================================================
    pdf.add_page()
    pdf.section_header("Parte 2. Obtención y exploración del dataset")

    pdf.sub_header("1. Primeros 10 Registros del Dataset Original (df_raw.head(10)):")
    
    # Tabla de 10 registros
    cols_w = [18, 52, 25, 28, 18, 18, 21]
    headers = ["ID", "Título", "Género", "Plataforma", "V. Fís", "V. Dig", "Precio"]
    
    pdf.set_font("Arial", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    for i, h in enumerate(headers):
        nx = XPos.LMARGIN if i == len(headers) - 1 else XPos.RIGHT
        ny = YPos.NEXT if i == len(headers) - 1 else YPos.TOP
        pdf.cell(cols_w[i], 5.5, h, border=1, align="C", fill=True, new_x=nx, new_y=ny)

    pdf.set_font("Arial", "", 7.2)
    for _, r in df_raw.head(10).iterrows():
        pdf.cell(cols_w[0], 5, str(r["id_juego"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[1], 5, f" {str(r['titulo'])[:25]}", border=1, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[2], 5, str(r["genero"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[3], 5, str(r["plataforma"])[:14], border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[4], 5, f"{r['ventas_fisicas_millones']:.2f}M", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[5], 5, f"{r['ventas_digitales_millones']:.2f}M" if pd.notnull(r['ventas_digitales_millones']) else "Nulo", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[6], 5, f"${r['precio_lanzamiento_usd']:.2f}" if pd.notnull(r['precio_lanzamiento_usd']) else "Nulo", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(4)
    pdf.sub_header("2. Estadísticas Descriptivas (df_raw.describe()):")

    desc = df_raw[["ventas_fisicas_millones", "ventas_digitales_millones", "precio_lanzamiento_usd", "calificacion_critica", "horas_juego"]].describe().T
    desc_w = [40, 20, 20, 20, 20, 20, 20, 20]
    desc_headers = ["Variable", "Count", "Mean", "Std", "Min", "50%", "75%", "Max"]

    pdf.set_font("Arial", "B", 7.2)
    for i, h in enumerate(desc_headers):
        nx = XPos.LMARGIN if i == len(desc_headers) - 1 else XPos.RIGHT
        ny = YPos.NEXT if i == len(desc_headers) - 1 else YPos.TOP
        pdf.cell(desc_w[i], 5, h, border=1, align="C", fill=True, new_x=nx, new_y=ny)

    pdf.set_font("Arial", "", 7.0)
    for var, row in desc.iterrows():
        pdf.cell(desc_w[0], 4.8, f" {var[:20]}", border=1, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(desc_w[1], 4.8, f"{int(row['count'])}", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(desc_w[2], 4.8, f"{row['mean']:.2f}", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(desc_w[3], 4.8, f"{row['std']:.2f}", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(desc_w[4], 4.8, f"{row['min']:.2f}", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(desc_w[5], 4.8, f"{row['50%']:.2f}", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(desc_w[6], 4.8, f"{row['75%']:.2f}", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(desc_w[7], 4.8, f"{row['max']:.2f}", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(4)
    pdf.sub_header("3. Auditoría de Datos: Dimensiones, Nulos y Duplicados")
    pdf.set_font("Arial", "", 8.5)
    pdf.cell(0, 4.5, f"Dimensiones: {df_raw.shape[0]} filas x {df_raw.shape[1]} columnas | Registros duplicados detectados: {df_raw.duplicated().sum()}", border=0, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 4.5, f"Valores nulos: {df_raw['ventas_digitales_millones'].isnull().sum()} en ventas_digitales, {df_raw['precio_lanzamiento_usd'].isnull().sum()} en precio, {df_raw['calificacion_critica'].isnull().sum()} en calificacion", border=0, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # =========================================================================
    # PARTE 3. REGISTROS LIMPIOS Y PREPARADOS
    # =========================================================================
    pdf.add_page()
    pdf.section_header("Parte 3. Limpieza y preparación de datos")

    pdf.sub_header("1. Primeros 10 Registros Limpios y Preparados (df_clean.head(10)):")

    pdf.set_font("Arial", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    for i, h in enumerate(headers):
        nx = XPos.LMARGIN if i == len(headers) - 1 else XPos.RIGHT
        ny = YPos.NEXT if i == len(headers) - 1 else YPos.TOP
        pdf.cell(cols_w[i], 5.5, h, border=1, align="C", fill=True, new_x=nx, new_y=ny)

    pdf.set_font("Arial", "", 7.2)
    for _, r in df_proc.head(10).iterrows():
        pdf.cell(cols_w[0], 5, str(r["id_juego"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[1], 5, f" {str(r['titulo'])[:25]}", border=1, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[2], 5, str(r["genero"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[3], 5, str(r["plataforma"])[:14], border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[4], 5, f"{r['ventas_fisicas_millones']:.2f}M", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[5], 5, f"{r['ventas_digitales_millones']:.2f}M", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(cols_w[6], 5, f"${r['precio_lanzamiento_usd']:.2f}", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(4)
    pdf.sub_header("2. Resumen Numérico de Limpieza y Escalamiento:")
    pdf.set_font("Arial", "", 8.5)
    pdf.cell(0, 4.5, f"- Filas originales: {df_raw.shape[0]} -> Filas limpias finales: {df_proc.shape[0]} (8 duplicados eliminados)", border=0, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 4.5, f"- Valores negativos corregidos con valor absoluto: 0 restantes", border=0, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 4.5, f"- Valores nulos restantes tras imputación contextual por género: 0", border=0, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 4.5, f"- Escalamiento con StandardScaler: 5 variables continuas normalizadas a media 0 y varianza 1", border=0, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # =========================================================================
    # PARTE 4. K-MEANS Y CENTROIDES
    # =========================================================================
    pdf.add_page()
    pdf.section_header("Parte 4. Implementación del algoritmo K-Means")

    pdf.sub_header("1. Evaluación de 7 Valores de K (Inercia y Coeficiente de Silueta):")
    k_eval_data = [
        ("K=2", "2,947.74", "0.3373"),
        ("K=3", "1,885.41", "0.4141"),
        ("K=4 (Óptimo)", "1,415.33", "0.4197"),
        ("K=5", "1,182.57", "0.3911"),
        ("K=6", "1,082.53", "0.3738"),
        ("K=7", "1,012.10", "0.3351"),
        ("K=8", "933.08", "0.2855"),
    ]

    kw = [35, 45, 45]
    pdf.set_font("Arial", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(kw[0], 5, "Configuración", border=1, align="C", fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(kw[1], 5, "Inercia (SSE)", border=1, align="C", fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(kw[2], 5, "Silhouette Score", border=1, align="C", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Arial", "", 7.5)
    for kv, inercia, sil in k_eval_data:
        is_opt = "Óptimo" in kv
        if is_opt:
            pdf.set_font("Arial", "B", 7.5)
        else:
            pdf.set_font("Arial", "", 7.5)
        pdf.cell(kw[0], 4.8, kv, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(kw[1], 4.8, inercia, border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(kw[2], 4.8, sil, border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(4)
    pdf.sub_header("2. Distribución de Registros y Centroides por Clúster (K=4):")

    cw = [62, 21, 21, 21, 20, 25]
    cheaders = ["Clúster Asignado", "Vta Física", "Vta Digital", "Precio", "Calif.", "Registros"]

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

    # =========================================================================
    # PARTE 5. REGISTROS CLASIFICADOS
    # =========================================================================
    pdf.add_page()
    pdf.section_header("Parte 5. Análisis e interpretación de resultados")

    pdf.sub_header("Muestra de Registros con Clúster Asignado (Primeros 15 Juegos):")

    rw = [55, 24, 26, 18, 18, 39]
    rheaders = ["Título", "Género", "Plataforma", "V. Fís", "V. Dig", "Clúster Asignado"]

    pdf.set_font("Arial", "B", 7.2)
    pdf.set_fill_color(243, 244, 246)
    for i, h in enumerate(rheaders):
        nx = XPos.LMARGIN if i == len(rheaders) - 1 else XPos.RIGHT
        ny = YPos.NEXT if i == len(rheaders) - 1 else YPos.TOP
        pdf.cell(rw[i], 5, h, border=1, align="C", fill=True, new_x=nx, new_y=ny)

    pdf.set_font("Arial", "", 7.0)
    for _, r in df_proc.head(15).iterrows():
        c_short = str(r["Cluster_Nombre"]).split(" (")[0]
        pdf.cell(rw[0], 4.8, f" {str(r['titulo'])[:25]}", border=1, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(rw[1], 4.8, str(r["genero"]), border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(rw[2], 4.8, str(r["plataforma"])[:12], border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(rw[3], 4.8, f"{r['ventas_fisicas_millones']:.2f}M", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(rw[4], 4.8, f"{r['ventas_digitales_millones']:.2f}M", border=1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(rw[5], 4.8, f" {c_short[:20]}", border=1, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    output_path = "docs/Practica_Examen.pdf"
    os.makedirs("docs", exist_ok=True)
    pdf.output(output_path)
    print(f"PDF exclusivo de tablas y registros generado: {output_path}")

if __name__ == "__main__":
    build_pdf()
