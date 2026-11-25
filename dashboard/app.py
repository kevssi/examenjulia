"""
GAMING SALES INTELLIGENCE: DASHBOARD ANALÍTICO EJECUTIVO
Segmentación Multivariada mediante K-Means | Mercado de Videojuegos Físicos vs. Digitales
Diseño Formal, Alto Contraste, Difuminados Glassmorphism e Iconografía Lucide (Sin emojis)
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Ventas del Formato Físico y Digital de los Videojuegos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# BIBLIOTECA DE ICONOS LUCIDE (SVG Vectoriales puros)
LUCIDE = {
    "layers": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>',
    "disc": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="3"></circle></svg>',
    "download": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>',
    "award": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg>',
    "sliders": '<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line></svg>',
    "chart_bar": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>',
    "pie_chart": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>',
    "scatter": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"></circle><circle cx="18.5" cy="5.5" r=".5" fill="currentColor"></circle><circle cx="11.5" cy="11.5" r=".5" fill="currentColor"></circle><circle cx="7.5" cy="16.5" r=".5" fill="currentColor"></circle><circle cx="17.5" cy="14.5" r=".5" fill="currentColor"></circle></svg>',
    "cpu": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'
}

# ESTILOS CSS DE ALTO CONTRASTE Y LEGIBILIDAD
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Fondo formal con difuminado suave */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 1) 90%);
        color: #F8FAFC;
    }

    /* Cabecera Principal */
    .main-header {
        padding: 6px 0 16px 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
        margin-bottom: 22px;
    }
    .main-title {
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-subtitle {
        font-size: 0.95rem;
        color: #CBD5E1;
        font-weight: 500;
        margin-top: 6px;
    }

    /* Tarjetas KPI con difuminado y alto contraste */
    .kpi-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-container:hover {
        border-color: rgba(96, 165, 250, 0.45);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .kpi-label {
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #94A3B8;
    }
    .kpi-icon {
        color: #60A5FA;
        display: inline-flex;
        align-items: center;
    }
    .kpi-number {
        font-size: 1.75rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }
    .kpi-detail {
        font-size: 0.78rem;
        color: #CBD5E1;
        margin-top: 5px;
    }

    /* CORRECCIÓN DE CONTRASTE TOTAL EN BARRA LATERAL */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1120 0%, #172033 100%) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.2) !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #F1F5F9 !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stSlider div[data-testid="stMarkdownContainer"] p {
        color: #F8FAFC !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stSlider div[data-baseweb="slider"] {
        margin-top: 4px;
    }
    [data-testid="stSidebar"] .stSlider span {
        color: #CBD5E1 !important;
        font-weight: 600 !important;
    }

    /* Tags del Multiselect con colores contrastados */
    [data-baseweb="tag"] {
        background-color: #1E293B !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 6px !important;
    }
    [data-baseweb="tag"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# 4 COLORES CORPORATIVOS VIVOS DE ALTO CONTRASTE (Cero confusión)
PALETA_CLUSTERS = {
    "Superventas Globales (Blockbusters - Alto Físico y Digital)": "#F43F5E",    # Rojo carmesí vibrante
    "Éxitos Digitales e Indies Virales (Alta Descarga, Bajo Físico)": "#3B82F6", # Azul eléctrico
    "Coleccionables de Consola (Físico Fuerte, Digital Moderado)": "#10B981",   # Verde esmeralda vivo
    "Fracasos Comerciales y Bajo Rendimiento (Ventas Bajas)": "#F59E0B"          # Ámbar dorado vivo
}

@st.cache_data
def load_data():
    csv_path = "data/videojuegos_ventas_procesado.csv"
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    return pd.read_csv(csv_path)

df = load_data()

if df.empty:
    st.error("No se encontró el dataset procesado de videojuegos. Ejecuta 'python src/process_kmeans_videojuegos.py'")
    st.stop()

# =============================================================================
# BARRA LATERAL: CONTROL DE NAVEGACIÓN Y FILTROS INTERACTIVOS
# =============================================================================
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; padding-bottom:12px; border-bottom:1px solid rgba(148,163,184,0.25); margin-bottom:16px;">
        <span style="color:#60A5FA;">{LUCIDE['cpu']}</span>
        <span style="font-size:1.15rem; font-weight:800; color:#FFFFFF;">Panel de Control</span>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegación:",
        options=["Análisis General de Ventas", "Segmentación K-Means de Rendimiento"],
        index=0
    )

    st.markdown("<hr style='border:none; border-top:1px solid rgba(148,163,184,0.2); margin:18px 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:6px; margin-bottom:12px;">
        <span style="color:#60A5FA;">{LUCIDE['sliders']}</span>
        <span style="font-size:0.85rem; font-weight:800; letter-spacing:0.06em; text-transform:uppercase; color:#60A5FA;">Filtros Multivariados</span>
    </div>
    """, unsafe_allow_html=True)

    # 1. Filtro por Clúster
    clusters_disponibles = sorted(df["Cluster_Nombre"].dropna().unique())
    sel_clusters = st.multiselect(
        "Clúster:",
        options=clusters_disponibles,
        default=clusters_disponibles
    )

    # 2. Filtro por Género
    generos_disponibles = sorted(df["genero"].dropna().unique())
    sel_generos = st.multiselect(
        "Género de Videojuego:",
        options=generos_disponibles,
        default=generos_disponibles
    )

    # 3. Filtro por Plataforma
    plataformas_disponibles = sorted(df["plataforma"].dropna().unique())
    sel_plataformas = st.multiselect(
        "Plataforma:",
        options=plataformas_disponibles,
        default=plataformas_disponibles
    )

    # 4. Slider de Precio de Lanzamiento (USD)
    min_prc = float(df["precio_lanzamiento_usd"].min())
    max_prc = float(df["precio_lanzamiento_usd"].max())
    sel_precio = st.slider(
        "Precio de Lanzamiento (USD):",
        min_value=min_prc,
        max_value=max_prc,
        value=(min_prc, max_prc),
        step=5.0
    )

    # 5. Slider de Calificación Crítica
    min_cal = int(df["calificacion_critica"].min())
    max_cal = int(df["calificacion_critica"].max())
    sel_calif = st.slider(
        "Calificación de la Crítica (0-100 pts):",
        min_value=min_cal,
        max_value=max_cal,
        value=(min_cal, max_cal),
        step=1
    )

# Aplicar filtros
df_filtro = df[
    (df["Cluster_Nombre"].isin(sel_clusters)) &
    (df["genero"].isin(sel_generos)) &
    (df["plataforma"].isin(sel_plataformas)) &
    (df["precio_lanzamiento_usd"] >= sel_precio[0]) &
    (df["precio_lanzamiento_usd"] <= sel_precio[1]) &
    (df["calificacion_critica"] >= sel_calif[0]) &
    (df["calificacion_critica"] <= sel_calif[1])
]

# =============================================================================
# CABECERA PRINCIPAL Y MÉTRICAS KPI EN TIEMPO REAL
# =============================================================================
st.markdown(f"""
<div class="main-header">
    <h1 class="main-title">{LUCIDE['layers']} Ventas del Formato Físico y Digital de los Videojuegos</h1>
    <div class="main-subtitle">
        Plataforma analítica y segmentación K-Means | Rendimiento comercial físico vs. digital
    </div>
</div>
""", unsafe_allow_html=True)

# 4 Tarjetas KPI
k1, k2, k3, k4 = st.columns(4)

total_obs = len(df_filtro)
total_universo = len(df)
med_dig = df_filtro["ventas_digitales_millones"].mean() if total_obs > 0 else 0
med_fis = df_filtro["ventas_fisicas_millones"].mean() if total_obs > 0 else 0
prom_calif = df_filtro["calificacion_critica"].mean() if total_obs > 0 else 0

with k1:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-header">
            <span class="kpi-label">Total Videojuegos</span>
            <span class="kpi-icon">{LUCIDE['layers']}</span>
        </div>
        <div class="kpi-number">{total_obs} <span style="font-size:0.95rem; font-weight:400; color:#94A3B8;">/ {total_universo}</span></div>
        <div class="kpi-detail">Catálogo visible tras aplicar filtros</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-header">
            <span class="kpi-label">Venta Digital Promedio</span>
            <span class="kpi-icon">{LUCIDE['download']}</span>
        </div>
        <div class="kpi-number">{med_dig:.2f} <span style="font-size:0.9rem; font-weight:600; color:#94A3B8;">M copias</span></div>
        <div class="kpi-detail">Descargas digitales por videojuego</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-header">
            <span class="kpi-label">Venta Física Promedio</span>
            <span class="kpi-icon">{LUCIDE['disc']}</span>
        </div>
        <div class="kpi-number">{med_fis:.2f} <span style="font-size:0.9rem; font-weight:600; color:#94A3B8;">M copias</span></div>
        <div class="kpi-detail">Discos y cartuchos en tienda física</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-header">
            <span class="kpi-label">Puntaje de Crítica</span>
            <span class="kpi-icon">{LUCIDE['award']}</span>
        </div>
        <div class="kpi-number">{prom_calif:.1f} <span style="font-size:0.9rem; font-weight:600; color:#94A3B8;">pts</span></div>
        <div class="kpi-detail">Promedio Metacritic de la prensa</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)

# Layout base oscuro formal para Plotly con CERO SOLAPAMIENTOS
layout_base = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15, 23, 42, 0.6)",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#E2E8F0", size=11),
    margin=dict(l=45, r=25, t=65, b=65),
    xaxis=dict(
        gridcolor="rgba(148, 163, 184, 0.15)",
        zerolinecolor="rgba(148, 163, 184, 0.3)",
        tickfont=dict(color="#CBD5E1", size=10),
        title_font=dict(color="#FFFFFF", size=11, weight="bold")
    ),
    yaxis=dict(
        gridcolor="rgba(148, 163, 184, 0.15)",
        zerolinecolor="rgba(148, 163, 184, 0.3)",
        tickfont=dict(color="#CBD5E1", size=10),
        title_font=dict(color="#FFFFFF", size=11, weight="bold")
    ),
    # LEYENDA EN LA PARTE INFERIOR PARA QUE NUNCA CHOQUE CON EL TÍTULO
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.22,
        xanchor="center",
        x=0.5,
        font=dict(color="#F1F5F9", size=10),
        title=dict(text="")
    )
)

# =============================================================================
# PÁGINA 1: ANÁLISIS GENERAL DE VENTAS FÍSICAS VS DIGITALES
# =============================================================================
if pagina == "Análisis General de Ventas":
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:16px;">
        <span style="color:#60A5FA;">{LUCIDE['chart_bar']}</span>
        <h3 style="margin:0; font-size:1.3rem; font-weight:800; color:#FFFFFF;">Exploración del Mercado: Ventas Físicas vs. Descargas Digitales</h3>
    </div>
    """, unsafe_allow_html=True)

    if total_obs == 0:
        st.warning("No hay registros que coincidan con los filtros seleccionados.")
    else:
        c_left, c_right = st.columns(2)

        # Gráfica 1: Dispersión Físico vs Digital coloreado por Clúster (MUY CLARO)
        with c_left:
            fig_disp = px.scatter(
                df_filtro,
                x="ventas_fisicas_millones",
                y="ventas_digitales_millones",
                color="Cluster_Nombre",
                size="calificacion_critica",
                color_discrete_map=PALETA_CLUSTERS,
                hover_data=["titulo", "plataforma", "genero", "ventas_totales_millones"],
                title="Relación de Ventas Físicas vs. Digitales por Clúster",
                labels={
                    "ventas_fisicas_millones": "Ventas Físicas (Millones de copias)",
                    "ventas_digitales_millones": "Ventas Digitales (Millones de copias)",
                    "Cluster_Nombre": "Clúster"
                }
            )
            fig_disp.update_layout(**layout_base)
            fig_disp.update_layout(
                title=dict(
                    text="Relación de Ventas Físicas vs. Digitales por Clúster",
                    x=0.01, y=0.96,
                    font=dict(size=13.5, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif")
                )
            )
            st.plotly_chart(fig_disp, width="stretch")

        # Gráfica 2: Comparativa de Ventas Físicas vs Digitales por Género (Barras Agrupadas)
        with c_right:
            gen_ventas = df_filtro.groupby("genero")[["ventas_fisicas_millones", "ventas_digitales_millones"]].mean().reset_index()
            gen_ventas = pd.melt(
                gen_ventas,
                id_vars=["genero"],
                value_vars=["ventas_fisicas_millones", "ventas_digitales_millones"],
                var_name="Canal",
                value_name="Ventas_Medias"
            )
            gen_ventas["Canal"] = gen_ventas["Canal"].map({
                "ventas_fisicas_millones": "Venta Física Media (M)",
                "ventas_digitales_millones": "Venta Digital Media (M)"
            })

            fig_bar_gen = px.bar(
                gen_ventas,
                x="genero",
                y="Ventas_Medias",
                color="Canal",
                barmode="group",
                color_discrete_map={
                    "Venta Física Media (M)": "#10B981", # Verde
                    "Venta Digital Media (M)": "#3B82F6"  # Azul
                },
                title="Promedio de Ventas Físicas vs. Digitales por Género",
                labels={"genero": "Género", "Ventas_Medias": "Millones de Copias Promedio"}
            )
            fig_bar_gen.update_layout(**layout_base)
            fig_bar_gen.update_layout(
                title=dict(
                    text="Promedio de Ventas Físicas vs. Digitales por Género",
                    x=0.01, y=0.96,
                    font=dict(size=13.5, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif")
                )
            )
            st.plotly_chart(fig_bar_gen, width="stretch")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        c_bar, c_heat = st.columns(2)

        # Gráfica 3: Ventas Totales por Plataforma (Barras Horizontales Ordenadas)
        with c_bar:
            plat_counts = df_filtro.groupby("plataforma")["ventas_totales_millones"].sum().reset_index()
            plat_counts = plat_counts.sort_values(by="ventas_totales_millones", ascending=True)

            fig_bar = px.bar(
                plat_counts,
                x="ventas_totales_millones",
                y="plataforma",
                orientation="h",
                text="ventas_totales_millones",
                title="Volumen Acumulado de Ventas por Plataforma",
                labels={"ventas_totales_millones": "Total Copias Vendidas (Millones)", "plataforma": "Plataforma"},
                color="ventas_totales_millones",
                color_continuous_scale="Blues"
            )
            fig_bar.update_layout(**layout_base)
            fig_bar.update_traces(texttemplate='%{text:.1f} M', textposition='outside', textfont=dict(color="#FFFFFF", size=10.5))
            fig_bar.update_coloraxes(showscale=False)
            fig_bar.update_layout(
                title=dict(
                    text="Volumen Acumulado de Ventas por Plataforma",
                    x=0.01, y=0.96,
                    font=dict(size=13.5, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif")
                )
            )
            st.plotly_chart(fig_bar, width="stretch")

        # Gráfica 4: Matriz de Correlación Numérica (Heatmap Claro con Nombres Limpios)
        with c_heat:
            cols_corr = ["ventas_fisicas_millones", "ventas_digitales_millones", "precio_lanzamiento_usd", "calificacion_critica", "horas_juego"]
            nombres_limpios = {
                "ventas_fisicas_millones": "Ventas Físicas",
                "ventas_digitales_millones": "Ventas Digitales",
                "precio_lanzamiento_usd": "Precio USD",
                "calificacion_critica": "Calificación",
                "horas_juego": "Horas Juego"
            }
            sub_df = df_filtro[cols_corr].rename(columns=nombres_limpios)
            corr_mat = sub_df.corr().round(2)

            fig_heat = px.imshow(
                corr_mat,
                text_auto=True,
                title="Matriz de Correlación Lineal Multivariada",
                color_continuous_scale="RdBu_r",
                zmin=-1, zmax=1
            )
            fig_heat.update_layout(**layout_base)
            fig_heat.update_coloraxes(showscale=False)
            fig_heat.update_layout(
                title=dict(
                    text="Matriz de Correlación Lineal Multivariada",
                    x=0.01, y=0.96,
                    font=dict(size=13.5, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif")
                )
            )
            st.plotly_chart(fig_heat, width="stretch")

# =============================================================================
# PÁGINA 2: SEGMENTACIÓN K-MEANS Y ARQUETIPOS DE NEGOCIO
# =============================================================================
else:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:16px;">
        <span style="color:#60A5FA;">{LUCIDE['pie_chart']}</span>
        <h3 style="margin:0; font-size:1.3rem; font-weight:800; color:#FFFFFF;">Segmentación No Supervisada: 4 Clústeres de Mercado (K=4)</h3>
    </div>
    """, unsafe_allow_html=True)

    if total_obs == 0:
        st.warning("No hay registros que coincidan con los filtros seleccionados.")
    else:
        # Fila 1: Dona de Proporción y Proyección PCA 2D
        c_pie, c_pca = st.columns([1, 1.4])

        with c_pie:
            cluster_dist = df_filtro["Cluster_Nombre"].value_counts().reset_index()
            cluster_dist.columns = ["Cluster_Nombre", "conteo"]

            fig_pie = px.pie(
                cluster_dist,
                names="Cluster_Nombre",
                values="conteo",
                hole=0.6,
                title="Proporción del Catálogo por Clúster",
                color="Cluster_Nombre",
                color_discrete_map=PALETA_CLUSTERS
            )
            fig_pie.update_layout(**layout_base)
            fig_pie.update_traces(
                textposition="inside",
                textinfo="percent",
                textfont=dict(size=12, color="#FFFFFF", family="Plus Jakarta Sans")
            )
            fig_pie.update_layout(
                title=dict(
                    text="Proporción del Catálogo por Clúster",
                    x=0.01, y=0.96,
                    font=dict(size=13.5, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif")
                )
            )
            st.plotly_chart(fig_pie, width="stretch")

        with c_pca:
            fig_pca = px.scatter(
                df_filtro,
                x="pca_x",
                y="pca_y",
                color="Cluster_Nombre",
                hover_data=["titulo", "ventas_totales_millones", "calificacion_critica"],
                title="Proyección de Clústeres (PCA 2D - 75.2% Varianza Explicada)",
                labels={
                    "pca_x": "Componente Principal 1 (Volumen y Calidad)",
                    "pca_y": "Componente Principal 2 (Preferencia Digital vs. Físico)",
                    "Cluster_Nombre": "Clúster"
                },
                color_discrete_map=PALETA_CLUSTERS
            )
            fig_pca.update_layout(**layout_base)
            fig_pca.update_layout(
                title=dict(
                    text="Proyección de Clústeres (PCA 2D - 75.2% Varianza Explicada)",
                    x=0.01, y=0.96,
                    font=dict(size=13.5, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif")
                )
            )
            st.plotly_chart(fig_pca, width="stretch")

        # Fila 2: Dos Gráficas Adicionales comparativas
        st.markdown("<hr style='border:none; border-top:1px solid rgba(148,163,184,0.2); margin:20px 0;'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
            <span style="color:#60A5FA;">{LUCIDE['chart_bar']}</span>
            <h4 style="margin:0; font-size:1.15rem; font-weight:800; color:#FFFFFF;">Comparación Multidimensional entre Clústeres</h4>
        </div>
        """, unsafe_allow_html=True)

        c_box, c_scat2 = st.columns(2)

        # Gráfica Adicional 1: Boxplot de Ventas Totales por Clúster
        with c_box:
            fig_box = px.box(
                df_filtro,
                x="Cluster_Nombre",
                y="ventas_totales_millones",
                color="Cluster_Nombre",
                color_discrete_map=PALETA_CLUSTERS,
                title="Dispersión del Volumen de Ventas Totales por Clúster",
                labels={"Cluster_Nombre": "Clúster", "ventas_totales_millones": "Ventas Totales (Millones de Copias)"}
            )
            fig_box.update_layout(**layout_base)
            fig_box.update_layout(
                showlegend=False,
                title=dict(
                    text="Dispersión del Volumen de Ventas Totales por Clúster",
                    x=0.01, y=0.96,
                    font=dict(size=13.5, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif")
                )
            )
            st.plotly_chart(fig_box, width="stretch")

        # Gráfica Adicional 2: Dispersión Ventas vs Calificación Crítica
        with c_scat2:
            fig_scat2 = px.scatter(
                df_filtro,
                x="calificacion_critica",
                y="ventas_totales_millones",
                color="Cluster_Nombre",
                size="precio_lanzamiento_usd",
                color_discrete_map=PALETA_CLUSTERS,
                hover_data=["titulo", "plataforma", "genero"],
                title="Relación entre Calificación Crítica y Ventas Totales",
                labels={"calificacion_critica": "Calificación Metacritic (Puntos)", "ventas_totales_millones": "Ventas Totales (Millones)"}
            )
            fig_scat2.update_layout(**layout_base)
            fig_scat2.update_layout(
                title=dict(
                    text="Relación entre Calificación Crítica y Ventas Totales",
                    x=0.01, y=0.96,
                    font=dict(size=13.5, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif")
                )
            )
            st.plotly_chart(fig_scat2, width="stretch")

# =============================================================================
# TABLA DE AUDITORÍA DE DATOS
# =============================================================================
st.markdown("<hr style='border:none; border-top:1px solid rgba(148,163,184,0.2); margin:24px 0 16px 0;'>", unsafe_allow_html=True)
with st.expander("Inspeccionar Catálogo Completo de Videojuegos Filtrados", expanded=False):
    st.dataframe(
        df_filtro[[
            "id_juego", "titulo", "genero", "plataforma", "distribuidora",
            "ventas_fisicas_millones", "ventas_digitales_millones", "ventas_totales_millones",
            "precio_lanzamiento_usd", "calificacion_critica", "horas_juego", "Cluster_Nombre"
        ]],
        width="stretch",
        height=320
    )
