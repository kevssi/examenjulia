"""
HYRULE DATA INSIGHTS: DASHBOARD ANALÍTICO EJECUTIVO
Segmentación Multivariada mediante K-Means | The Legend of Zelda Compendium
Diseño Formal, Difuminados Glassmorphism e Iconografía Lucide
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Hyrule Data Insights | Segmentación K-Means",
    layout="wide",
    initial_sidebar_state="expanded"
)

# BIBLIOTECA DE ICONOS LUCIDE (SVG Vectoriales puros)
LUCIDE = {
    "layers": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>',
    "sword": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="14.5 17.5 3 6 3 3 6 3 17.5 14.5"></polyline><line x1="13" y1="19" x2="19" y2="13"></line><line x1="16" y1="16" x2="20" y2="20"></line><line x1="19" y1="21" x2="21" y2="19"></line></svg>',
    "shield": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
    "clock": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>',
    "coins": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="6"></circle><path d="M18.09 10.37A6 6 0 1 1 10.34 18"></path><path d="M7 6h1v4"></path><path d="M16.7 13.77h.01"></path></svg>',
    "sliders": '<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line></svg>',
    "chart_bar": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>',
    "pie_chart": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>',
    "scatter": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"></circle><circle cx="18.5" cy="5.5" r=".5" fill="currentColor"></circle><circle cx="11.5" cy="11.5" r=".5" fill="currentColor"></circle><circle cx="7.5" cy="16.5" r=".5" fill="currentColor"></circle><circle cx="17.5" cy="14.5" r=".5" fill="currentColor"></circle></svg>',
    "cpu": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>',
    "compass": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon></svg>',
    "info": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>',
    "check_circle": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
    "award": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg>'
}

# ESTILOS CSS FORMALES CON DIFUMINADOS Y GLASSMORPHISM (Sin emojis)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Fondo formal con difuminado suave */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 1) 90%);
        color: #F8FAFC;
    }

    /* Cabecera Principal */
    .main-header {
        padding: 6px 0 16px 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        margin-bottom: 22px;
    }
    .main-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #F8FAFC;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .main-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        font-weight: 400;
        margin-top: 4px;
    }

    /* Tarjetas KPI con difuminado (Glassmorphism formal) */
    .kpi-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.75) 100%);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.25), 0 0 15px rgba(59, 130, 246, 0.03);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-container:hover {
        border-color: rgba(99, 102, 241, 0.3);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
    }
    .kpi-icon {
        color: #60A5FA;
        display: inline-flex;
        align-items: center;
    }
    .kpi-number {
        font-size: 1.65rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }
    .kpi-detail {
        font-size: 0.78rem;
        color: #64748B;
        margin-top: 4px;
    }

    /* Tarjetas descriptivas de Clústeres */
    .cluster-profile-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.65) 100%);
        backdrop-filter: blur(12px);
        border-radius: 10px;
        padding: 18px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-left: 4px solid #3B82F6;
        margin-bottom: 14px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    .cluster-title {
        font-size: 0.98rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0 0 8px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .cluster-desc {
        font-size: 0.85rem;
        color: #CBD5E1;
        line-height: 1.5;
        margin: 0;
    }
    .cluster-tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-top: 8px;
        background: rgba(255, 255, 255, 0.06);
        color: #94A3B8;
    }

    /* Cajas informativas formales */
    .insight-box {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 8px;
        padding: 14px 16px;
        font-size: 0.87rem;
        color: #E2E8F0;
        line-height: 1.55;
    }
    .insight-bullet {
        margin-bottom: 8px;
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }

    /* Reducción de espaciados */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# CARGA DE DATOS CON CACHÉ
@st.cache_data
def load_compendium():
    csv_path = "data/zelda_hyrule_compendium_procesado.csv"
    if not os.path.exists(csv_path):
        csv_path = "../data/zelda_hyrule_compendium_procesado.csv"
    df = pd.read_csv(csv_path)

    json_path = "data/model_summary.json"
    if not os.path.exists(json_path):
        json_path = "../data/model_summary.json"
    
    summary = {}
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            summary = json.load(f)
            
    return df, summary

df_all, model_summary = load_compendium()

# PALETA FORMAL PARA CLÚSTERES (Equilibrada, seria y de alto contraste)
FORMAL_CLUSTER_PALETTE = {
    "Arsenal Ofensivo y Armas de Asalto": "#E11D48",              # Carmesí Formal
    "Blindaje Táctico, Armaduras y Escudos": "#2563EB",            # Azul Cobalto Formal
    "Recursos Básicos, Forraje y Consumibles": "#059669",          # Verde Esmeralda Formal
    "Jefes Supremos, Calamidades y Reliquias Míticas": "#D97706"   # Ámbar Bronce Formal
}

# BARRA LATERAL: NAVEGACIÓN Y FILTROS INTERACTIVOS FORMALES
st.sidebar.markdown(f"""
<div style='display:flex; align-items:center; gap:8px; padding-bottom: 12px; border-bottom: 1px solid rgba(148,163,184,0.15);'>
    <span style='color:#60A5FA;'>{LUCIDE['cpu']}</span>
    <span style='font-weight:700; font-size:1rem; color:#F8FAFC;'>Panel de Control</span>
</div>
""", unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "Navegación:",
    ["Análisis General", "Segmentación K-Means"],
    index=0
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div style='display:flex; align-items:center; gap:6px; margin-bottom:10px;'>
    <span style='color:#94A3B8;'>{LUCIDE['sliders']}</span>
    <span style='font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#94A3B8;'>Filtros Multivariados</span>
</div>
""", unsafe_allow_html=True)

# Filtro 1: Clústeres
clusters_disponibles = sorted(df_all["Cluster_Nombre"].unique())
sel_clusters = st.sidebar.multiselect(
    "Clúster:",
    options=clusters_disponibles,
    default=clusters_disponibles
)

# Filtro 2: Categorías
categorias_disponibles = sorted(df_all["category"].unique())
sel_categorias = st.sidebar.multiselect(
    "Categoría de Ítem:",
    options=categorias_disponibles,
    default=categorias_disponibles
)

# Filtro 3: Rango de Precio en Rupias
min_p, max_p = int(df_all["sell_price"].min()), int(df_all["sell_price"].max())
sel_precio = st.sidebar.slider(
    "Precio en Rupias:",
    min_value=min_p,
    max_value=max_p,
    value=(min_p, max_p),
    step=50
)

# Filtro 4: Nivel de Rareza
sel_rareza = st.sidebar.slider(
    "Nivel de Rareza (Tier 1 a 5):",
    min_value=1,
    max_value=5,
    value=(1, 5)
)

# Aplicar filtros
df_filtered = df_all[
    (df_all["Cluster_Nombre"].isin(sel_clusters)) &
    (df_all["category"].isin(sel_categorias)) &
    (df_all["sell_price"] >= sel_precio[0]) &
    (df_all["sell_price"] <= sel_precio[1]) &
    (df_all["rarity_tier"] >= sel_rareza[0]) &
    (df_all["rarity_tier"] <= sel_rareza[1])
]

# CABECERA FORMAL
st.markdown(f"""
<div class='main-header'>
    <div class='main-title'>
        <span style='color:#38BDF8;'>{LUCIDE['layers']}</span>
        <span>Hyrule Data Insights</span>
    </div>
    <div class='main-subtitle'>
        Plataforma analítica de segmentación no supervisada mediante K-Means y auditoría multivariada
    </div>
</div>
""", unsafe_allow_html=True)

# CUATRO INDICADORES KPI RELEVANTES CON DIFUMINADO Y LUCIDE ICONS (Requerimiento Parte 6)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class='kpi-container'>
        <div class='kpi-header'>
            <span class='kpi-label'>Total Observaciones</span>
            <span class='kpi-icon'>{LUCIDE['layers']}</span>
        </div>
        <div class='kpi-number'>{len(df_filtered)} <span style='font-size:0.9rem; color:#64748B;'>/ {len(df_all)}</span></div>
        <div class='kpi-detail'>Ítems analizados en catálogo</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    mean_atk = df_filtered["attack_power"].mean() if len(df_filtered) > 0 else 0
    st.markdown(f"""
    <div class='kpi-container'>
        <div class='kpi-header'>
            <span class='kpi-label'>Poder Ofensivo Promedio</span>
            <span class='kpi-icon'>{LUCIDE['sword']}</span>
        </div>
        <div class='kpi-number'>{mean_atk:.1f} <span style='font-size:0.9rem; color:#64748B;'>pts</span></div>
        <div class='kpi-detail'>Capacidad de impacto en combate</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    med_dur = df_filtered["durability"].median() if len(df_filtered) > 0 else 0
    st.markdown(f"""
    <div class='kpi-container'>
        <div class='kpi-header'>
            <span class='kpi-label'>Durabilidad Mediana</span>
            <span class='kpi-icon'>{LUCIDE['clock']}</span>
        </div>
        <div class='kpi-number'>{med_dur:.0f} <span style='font-size:0.9rem; color:#64748B;'>pts</span></div>
        <div class='kpi-detail'>Resistencia y ciclo de vida</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    mean_prc = df_filtered["sell_price"].mean() if len(df_filtered) > 0 else 0
    st.markdown(f"""
    <div class='kpi-container'>
        <div class='kpi-header'>
            <span class='kpi-label'>Valoración Promedio</span>
            <span class='kpi-icon'>{LUCIDE['coins']}</span>
        </div>
        <div class='kpi-number'>{mean_prc:.0f} <span style='font-size:0.9rem; color:#64748B;'>Rupias</span></div>
        <div class='kpi-detail'>Precio medio en economía mercantil</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if len(df_filtered) == 0:
    st.info("No se hallaron registros que coincidan con los filtros aplicados. Modifique los parámetros en la barra lateral.")
    st.stop()

# ==============================================================================
# PÁGINA 1: ANÁLISIS GENERAL
# ==============================================================================
if pagina == "Análisis General":
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:8px; margin-bottom:12px;'>
        <span style='color:#38BDF8;'>{LUCIDE['chart_bar']}</span>
        <h3 style='margin:0; font-size:1.25rem; font-weight:700; color:#F8FAFC;'>Página 1: Análisis General del Compendio</h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:6px; margin-bottom:6px;'>
            <span style='color:#94A3B8;'>{LUCIDE['sword']}</span>
            <span style='font-weight:600; font-size:0.9rem; color:#E2E8F0;'>Distribución de Daño Ofensivo por Categoría</span>
        </div>
        """, unsafe_allow_html=True)
        fig_hist = px.histogram(
            df_filtered,
            x="attack_power",
            color="category",
            nbins=28,
            template="plotly_dark",
            barmode="overlay",
            opacity=0.75,
            labels={"attack_power": "Poder de Ataque (Puntos)", "count": "Frecuencia"}
        )
        fig_hist.update_layout(
            margin=dict(l=20, r=20, t=10, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10))
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with c2:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:6px; margin-bottom:6px;'>
            <span style='color:#94A3B8;'>{LUCIDE['coins']}</span>
            <span style='font-weight:600; font-size:0.9rem; color:#E2E8F0;'>Relación entre Durabilidad y Precio de Venta</span>
        </div>
        """, unsafe_allow_html=True)
        fig_scatter_gen = px.scatter(
            df_filtered,
            x="durability",
            y="sell_price",
            color="category",
            size="rarity_tier",
            hover_name="item_name",
            hover_data=["origin_region", "attack_power", "defense_power"],
            template="plotly_dark",
            labels={"durability": "Durabilidad / HP", "sell_price": "Precio (Rupias)"}
        )
        fig_scatter_gen.update_layout(
            margin=dict(l=20, r=20, t=10, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10))
        )
        st.plotly_chart(fig_scatter_gen, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:6px; margin-bottom:6px;'>
            <span style='color:#94A3B8;'>{LUCIDE['compass']}</span>
            <span style='font-weight:600; font-size:0.9rem; color:#E2E8F0;'>Distribución Geográfica de Ítems por Región</span>
        </div>
        """, unsafe_allow_html=True)
        reg_df = df_filtered["origin_region"].value_counts().reset_index()
        reg_df.columns = ["Región", "Registros"]
        fig_reg = px.bar(
            reg_df,
            x="Registros",
            y="Región",
            orientation="h",
            color="Registros",
            color_continuous_scale="Blues",
            template="plotly_dark"
        )
        fig_reg.update_layout(
            margin=dict(l=20, r=20, t=10, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with c4:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:6px; margin-bottom:6px;'>
            <span style='color:#94A3B8;'>{LUCIDE['scatter']}</span>
            <span style='font-weight:600; font-size:0.9rem; color:#E2E8F0;'>Matriz de Correlación Numérica de Atributos</span>
        </div>
        """, unsafe_allow_html=True)
        corr_cols = ["attack_power", "defense_power", "durability", "sell_price", "rarity_tier"]
        corr_df = df_filtered[corr_cols].corr()
        fig_corr = px.imshow(
            corr_df,
            text_auto=".2f",
            color_continuous_scale="Blues",
            template="plotly_dark",
            aspect="auto"
        )
        fig_corr.update_layout(
            margin=dict(l=20, r=20, t=10, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:6px; margin-top:16px; margin-bottom:8px;'>
        <span style='color:#94A3B8;'>{LUCIDE['layers']}</span>
        <span style='font-weight:600; font-size:0.95rem; color:#E2E8F0;'>Catálogo de Datos Tabular</span>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(
        df_filtered[["item_id", "item_name", "category", "subcategory", "attack_power", "defense_power", "durability", "sell_price", "rarity_tier", "origin_region"]],
        use_container_width=True,
        height=260
    )

# ==============================================================================
# PÁGINA 2: SEGMENTACIÓN K-MEANS
# ==============================================================================
else:
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:8px; margin-bottom:12px;'>
        <span style='color:#38BDF8;'>{LUCIDE['cpu']}</span>
        <h3 style='margin:0; font-size:1.25rem; font-weight:700; color:#F8FAFC;'>Página 2: Segmentación y Clústeres K-Means</h3>
    </div>
    """, unsafe_allow_html=True)

    # 1. Gráfica de distribución de registros por clúster (Requerimiento)
    # 2. Gráfica de dispersión para visualizar agrupamientos (Requerimiento)
    col_dist, col_scat = st.columns([1, 2])

    with col_dist:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:6px; margin-bottom:6px;'>
            <span style='color:#94A3B8;'>{LUCIDE['pie_chart']}</span>
            <span style='font-weight:600; font-size:0.9rem; color:#E2E8F0;'>Proporción por Clúster</span>
        </div>
        """, unsafe_allow_html=True)
        cluster_counts = df_filtered["Cluster_Nombre"].value_counts().reset_index()
        cluster_counts.columns = ["Clúster", "Cantidad"]
        fig_donut = px.pie(
            cluster_counts,
            names="Clúster",
            values="Cantidad",
            color="Clúster",
            color_discrete_map=FORMAL_CLUSTER_PALETTE,
            hole=0.55,
            template="plotly_dark"
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent')
        fig_donut.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=9))
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_scat:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:6px; margin-bottom:6px;'>
            <span style='color:#94A3B8;'>{LUCIDE['scatter']}</span>
            <span style='font-weight:600; font-size:0.9rem; color:#E2E8F0;'>Proyección de Clústeres (PCA 2D - 70.8% Varianza Explicada)</span>
        </div>
        """, unsafe_allow_html=True)
        fig_pca = px.scatter(
            df_filtered,
            x="pca_x",
            y="pca_y",
            color="Cluster_Nombre",
            color_discrete_map=FORMAL_CLUSTER_PALETTE,
            hover_name="item_name",
            hover_data=["category", "attack_power", "defense_power", "durability", "sell_price"],
            labels={"pca_x": "Componente Principal 1 (Daño Ofensivo)", "pca_y": "Componente Principal 2 (Blindaje y Precio)"},
            template="plotly_dark",
            opacity=0.8
        )
        fig_pca.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9))
        )
        st.plotly_chart(fig_pca, use_container_width=True)

    # DOS GRÁFICAS ADICIONALES PARA COMPARAR CARACTERÍSTICAS (Requerimiento Parte 6)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:6px; margin-bottom:8px;'>
        <span style='color:#38BDF8;'>{LUCIDE['chart_bar']}</span>
        <span style='font-weight:700; font-size:1.05rem; color:#F8FAFC;'>Comparación Multidimensional entre Clústeres</span>
    </div>
    """, unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:6px; margin-bottom:4px;'>
            <span style='color:#94A3B8;'>{LUCIDE['sword']}</span>
            <span style='font-weight:600; font-size:0.88rem; color:#CBD5E1;'>Gráfica Adicional 1: Dispersión del Poder Ofensivo</span>
        </div>
        """, unsafe_allow_html=True)
        fig_box = px.box(
            df_filtered,
            x="Cluster_Nombre",
            y="attack_power",
            color="Cluster_Nombre",
            color_discrete_map=FORMAL_CLUSTER_PALETTE,
            template="plotly_dark",
            labels={"Cluster_Nombre": "Clúster", "attack_power": "Poder de Ataque"}
        )
        fig_box.update_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_tickangle=-15
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with g2:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:6px; margin-bottom:4px;'>
            <span style='color:#94A3B8;'>{LUCIDE['coins']}</span>
            <span style='font-weight:600; font-size:0.88rem; color:#CBD5E1;'>Gráfica Adicional 2: Relación Ataque vs Precio en Rupias</span>
        </div>
        """, unsafe_allow_html=True)
        fig_scat_prc = px.scatter(
            df_filtered,
            x="attack_power",
            y="sell_price",
            color="Cluster_Nombre",
            color_discrete_map=FORMAL_CLUSTER_PALETTE,
            size="rarity_tier",
            hover_name="item_name",
            template="plotly_dark",
            labels={"attack_power": "Poder de Ataque", "sell_price": "Precio (Rupias)"}
        )
        fig_scat_prc.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9))
        )
        st.plotly_chart(fig_scat_prc, use_container_width=True)

    # TABLA CON ESTADÍSTICAS DESCRIPTIVAS DE LOS CLÚSTERES (Requerimiento Parte 6)
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:6px; margin-top:16px; margin-bottom:8px;'>
        <span style='color:#38BDF8;'>{LUCIDE['layers']}</span>
        <span style='font-weight:700; font-size:1.05rem; color:#F8FAFC;'>Estadísticas Descriptivas por Clúster</span>
    </div>
    """, unsafe_allow_html=True)
    features_stats = ["attack_power", "defense_power", "durability", "sell_price", "rarity_tier"]
    stats_table = df_filtered.groupby("Cluster_Nombre")[features_stats].agg(["mean", "median", "std"]).round(1)
    st.dataframe(stats_table, use_container_width=True)

    # SECCIÓN CON LA DESCRIPCIÓN DE LOS GRUPOS IDENTIFICADOS (Requerimiento Parte 6)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:6px; margin-bottom:12px;'>
        <span style='color:#38BDF8;'>{LUCIDE['shield']}</span>
        <span style='font-weight:700; font-size:1.05rem; color:#F8FAFC;'>Descripción de los Grupos Identificados</span>
    </div>
    """, unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        st.markdown(f"""
        <div class='cluster-profile-card' style='border-left-color: #E11D48;'>
            <div class='cluster-title'>
                <span style='color:#E11D48;'>{LUCIDE['sword']}</span>
                <span>Arsenal Ofensivo y Armas de Asalto</span>
            </div>
            <p class='cluster-desc'>
                <b>Perfil Cuantitativo:</b> Ataque elevado (media 47.8 pts), defensa nula (0.7 pts), durabilidad media (57.7 pts) y coste de 571 Rupias.<br>
                <b>Función Táctica:</b> Concentra espadas, mandobles, lanzas de combate y arcos de repetición destinados a infligir daño activo inmediato en combate.
            </p>
            <span class='cluster-tag'>Población: 432 ítems (45.6%)</span>
        </div>

        <div class='cluster-profile-card' style='border-left-color: #059669;'>
            <div class='cluster-title'>
                <span style='color:#059669;'>{LUCIDE['layers']}</span>
                <span>Recursos Básicos, Forraje y Consumibles</span>
            </div>
            <p class='cluster-desc'>
                <b>Perfil Cuantitativo:</b> Ataque bajo (media 8.1 pts), defensa reducida (5.0 pts), durabilidad mínima (33.1 pts) y coste de 134 Rupias.<br>
                <b>Función Táctica:</b> Setas, hierbas, frutas, elixires, recetas de sustento y botín común. Base fundamental de forrajeo y supervivencia.
            </p>
            <span class='cluster-tag'>Población: 344 ítems (36.3%)</span>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown(f"""
        <div class='cluster-profile-card' style='border-left-color: #2563EB;'>
            <div class='cluster-title'>
                <span style='color:#2563EB;'>{LUCIDE['shield']}</span>
                <span>Blindaje Táctico, Armaduras y Escudos</span>
            </div>
            <p class='cluster-desc'>
                <b>Perfil Cuantitativo:</b> Ataque casi nulo (1.1 pts), máxima absorción defensiva (media 43.1 pts), durabilidad destacada (104.7 pts) y precio elevado (1,433 Rupias).<br>
                <b>Función Táctica:</b> Escudos metálicos pesados y armaduras de Gran Hada orientados a mitigar impactos y ejecutar parry.
            </p>
            <span class='cluster-tag'>Población: 138 ítems (14.6%)</span>
        </div>

        <div class='cluster-profile-card' style='border-left-color: #D97706;'>
            <div class='cluster-title'>
                <span style='color:#D97706;'>{LUCIDE['award']}</span>
                <span>Jefes Supremos, Calamidades y Reliquias Míticas</span>
            </div>
            <p class='cluster-desc'>
                <b>Perfil Cuantitativo:</b> Máximo poder de daño (75.7 pts), alta defensa (47.2 pts), colosal durabilidad de combate (706.2 pts) y rareza Tier 5.<br>
                <b>Función Táctica:</b> Representa jefes de campo (Lynels Plateados/Dorados, Calamity Ganon, Molduras) y equipamiento de élite absoluto.
            </p>
            <span class='cluster-tag'>Población: 33 ítems (3.5%)</span>
        </div>
        """, unsafe_allow_html=True)

    # SECCIÓN CON LOS PRINCIPALES HALLAZGOS Y RECOMENDACIONES (Requerimiento Parte 6)
    st.markdown("<br>", unsafe_allow_html=True)
    h1, h2 = st.columns(2)

    with h1:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:6px; margin-bottom:8px;'>
            <span style='color:#38BDF8;'>{LUCIDE['info']}</span>
            <span style='font-weight:700; font-size:1rem; color:#F8FAFC;'>Hallazgos Principales del Modelo</span>
        </div>
        <div class='insight-box'>
            <div class='insight-bullet'>
                <span style='color:#60A5FA; margin-top:2px;'>{LUCIDE['check_circle']}</span>
                <span><b>Polarización Ofensiva-Defensiva Binaria:</b> No existen ítems equilibrados en daño y protección; el catálogo obliga a alternar roles activos de ataque y defensa.</span>
            </div>
            <div class='insight-bullet'>
                <span style='color:#60A5FA; margin-top:2px;'>{LUCIDE['check_circle']}</span>
                <span><b>Asimetría Comercial de la Protección:</b> El blindaje pasivo tiene un coste casi tres veces superior al de las armas ofensivas (1,433 vs 571 Rupias).</span>
            </div>
            <div class='insight-bullet'>
                <span style='color:#60A5FA; margin-top:2px;'>{LUCIDE['check_circle']}</span>
                <span><b>Concentración Extrema de Dificultad:</b> El Clúster 3 comprende solo el 3.5% del juego pero posee 12 veces más vida útil que el resto de las entidades.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with h2:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:6px; margin-bottom:8px;'>
            <span style='color:#10B981;'>{LUCIDE['check_circle']}</span>
            <span style='font-weight:700; font-size:1rem; color:#F8FAFC;'>Recomendaciones Estratégicas</span>
        </div>
        <div class='insight-box'>
            <div class='insight-bullet'>
                <span style='color:#10B981; margin-top:2px;'>{LUCIDE['check_circle']}</span>
                <span><b>Configuración de Inventario:</b> Priorizar un ratio de ranuras 60% Armamento de Asalto, 25% Blindaje Táctico y 15% Recursos Potenciadores.</span>
            </div>
            <div class='insight-bullet'>
                <span style='color:#10B981; margin-top:2px;'>{LUCIDE['check_circle']}</span>
                <span><b>Balance de Economía de Juego:</b> Ajustar al alza el precio de venta de las espadas de élite para reducir la brecha comercial frente a armaduras.</span>
            </div>
            <div class='insight-bullet'>
                <span style='color:#10B981; margin-top:2px;'>{LUCIDE['check_circle']}</span>
                <span><b>Curva de Progresión Escalonada:</b> Diseñar entidades intermedias (200-350 HP) para suavizar la dificultad previa a los Jefes de Calamidad.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: rgba(148, 163, 184, 0.1); margin-top: 20px; margin-bottom: 12px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 0.8rem; margin:0;'>Proyecto Integrador de Minería de Datos | Segmentación K-Means | The Legend of Zelda Universe</p>", unsafe_allow_html=True)
