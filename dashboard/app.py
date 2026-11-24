"""
⚔️ HYRULE DATA INSIGHTS: DASHBOARD INTERACTIVO
Segmentación mediante K-Means de Equipamiento, Monstruos y Recursos en The Legend of Zelda
Proyecto Integrador - Minería de Datos
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
    page_title="Hyrule Data Insights | K-Means Zelda",
    page_icon="🗡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados inspirados en The Legend of Zelda (Breath of the Wild / TotK)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Nunito:wght@400;600;700&display=swap');
    
    .zelda-title {
        font-family: 'Cinzel', serif;
        font-size: 2.3rem;
        font-weight: 900;
        color: #C5A059;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
        margin-bottom: 0px;
    }
    .zelda-sub {
        font-family: 'Nunito', sans-serif;
        font-size: 1.1rem;
        color: #7A8B99;
        margin-bottom: 20px;
    }
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(197, 160, 89, 0.4);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .kpi-val {
        font-family: 'Cinzel', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #FACC15;
    }
    .kpi-lbl {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .cluster-card {
        background-color: rgba(30, 41, 59, 0.5);
        border-left: 5px solid #C5A059;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Carga de datos con caché
@st.cache_data
def load_data():
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

df_all, model_summary = load_data()

# PALETA OFICIAL DE CLÚSTERES DE HYRULE
CLUSTER_COLORS = {
    "Arsenal Ofensivo y Armas de Asalto": "#EF4444",              # Rojo Carmesí
    "Blindaje Táctico, Armaduras y Escudos": "#3B82F6",            # Azul Zora
    "Recursos Básicos, Forraje y Consumibles": "#10B981",          # Verde Bosque Korok
    "Jefes Supremos, Calamidades y Reliquias Míticas": "#F59E0B"   # Oro Antiguo / Calamidad
}

# SIDEBAR: NAVEGACIÓN Y FILTROS INTERACTIVOS
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/0e/Zelda_Triforce.svg", width=60)
st.sidebar.markdown("### **Reino de Hyrule | Control**")
pagina = st.sidebar.radio(
    "Selecciona la Página:",
    ["Página 1: Análisis General", "Página 2: Segmentación mediante K-Means"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Filtros Interactivos")

# Filtro 1: Clústeres
clusters_disponibles = sorted(df_all["Cluster_Nombre"].unique())
sel_clusters = st.sidebar.multiselect(
    "1. Filtrar por Clúster:",
    options=clusters_disponibles,
    default=clusters_disponibles
)

# Filtro 2: Categorías
categorias_disponibles = sorted(df_all["category"].unique())
sel_categorias = st.sidebar.multiselect(
    "2. Filtrar por Categoría:",
    options=categorias_disponibles,
    default=categorias_disponibles
)

# Filtro 3: Rango de Precio en Rupias
min_p, max_p = int(df_all["sell_price"].min()), int(df_all["sell_price"].max())
sel_precio = st.sidebar.slider(
    "3. Rango de Precio (Rupias ₹):",
    min_value=min_p,
    max_value=max_p,
    value=(min_p, max_p),
    step=20
)

# Filtro 4: Nivel de Rareza
sel_rareza = st.sidebar.slider(
    "4. Tier de Rareza (1 a 5):",
    min_value=1,
    max_value=5,
    value=(1, 5)
)

# Aplicación de filtros
df_filtered = df_all[
    (df_all["Cluster_Nombre"].isin(sel_clusters)) &
    (df_all["category"].isin(sel_categorias)) &
    (df_all["sell_price"] >= sel_precio[0]) &
    (df_all["sell_price"] <= sel_precio[1]) &
    (df_all["rarity_tier"] >= sel_rareza[0]) &
    (df_all["rarity_tier"] <= sel_rareza[1])
]

# CABECERA PRINCIPAL
st.markdown("<h1 class='zelda-title'>⚔️ The Legend of Zelda: Hyrule Data Insights 🛡️</h1>", unsafe_allow_html=True)
st.markdown("<p class='zelda-sub'>Segmentación no supervisada mediante K-Means y visualización interactiva del Compendio de Hyrule</p>", unsafe_allow_html=True)

# CUATRO INDICADORES KPI RELEVANTES (Requerimiento Parte 6)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-lbl'>Total Ítems Filtrados</div>
        <div class='kpi-val'>{len(df_filtered)} <span style='font-size:1rem;color:#94a3b8;'>/ {len(df_all)}</span></div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    atk_mean = df_filtered["attack_power"].mean() if len(df_filtered) > 0 else 0
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-lbl'>Poder de Ataque Medio</div>
        <div class='kpi-val'>🗡️ {atk_mean:.1f} <span style='font-size:1rem;color:#94a3b8;'>dmg</span></div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    dur_med = df_filtered["durability"].median() if len(df_filtered) > 0 else 0
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-lbl'>Durabilidad Mediana</div>
        <div class='kpi-val'>⏳ {dur_med:.0f} <span style='font-size:1rem;color:#94a3b8;'>pts</span></div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    price_mean = df_filtered["sell_price"].mean() if len(df_filtered) > 0 else 0
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-lbl'>Precio Promedio</div>
        <div class='kpi-val'>💎 {price_mean:.0f} <span style='font-size:1rem;color:#94a3b8;'>₹</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if len(df_filtered) == 0:
    st.warning("⚠️ No se encontraron registros con los filtros seleccionados. Por favor ajusta los filtros en la barra lateral.")
    st.stop()

# ==============================================================================
# PÁGINA 1: ANÁLISIS GENERAL
# ==============================================================================
if pagina == "Página 1: Análisis General":
    st.header("📊 Página 1: Análisis General del Ecosistema de Hyrule")
    st.markdown("Exploración global de la distribución de estadísticas de combate, valor económico y distribución geográfica en el reino de Hyrule.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🗡️ Distribución de Ataque y Defensa")
        fig_hist = px.histogram(
            df_filtered,
            x="attack_power",
            color="category",
            nbins=30,
            title="Distribución de Poder de Ataque por Categoría",
            labels={"attack_power": "Poder de Ataque (Daño)", "count": "Cantidad de Ítems"},
            template="plotly_dark",
            barmode="overlay",
            opacity=0.75
        )
        fig_hist.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_hist, use_container_width=True)

    with c2:
        st.subheader("💎 Economía de Hyrule: Precio vs Durabilidad")
        fig_scatter_gen = px.scatter(
            df_filtered,
            x="durability",
            y="sell_price",
            color="category",
            size="rarity_tier",
            hover_name="item_name",
            hover_data=["origin_region", "attack_power", "defense_power"],
            title="Relación entre Resistencia y Precio de Venta en Rupias",
            labels={"durability": "Durabilidad (Vida Útil / HP)", "sell_price": "Precio en Rupias (₹)"},
            template="plotly_dark"
        )
        st.plotly_chart(fig_scatter_gen, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("🗺️ Cantidad de Recursos por Región de Origen")
        region_counts = df_filtered["origin_region"].value_counts().reset_index()
        region_counts.columns = ["Región", "Cantidad"]
        fig_bar_reg = px.bar(
            region_counts,
            x="Región",
            y="Cantidad",
            color="Región",
            title="Abundancia de Ítems por Región de Hyrule",
            template="plotly_dark"
        )
        fig_bar_reg.update_layout(showlegend=False)
        st.plotly_chart(fig_bar_reg, use_container_width=True)

    with c4:
        st.subheader("🔥 Matriz de Correlación de Atributos")
        corr_cols = ["attack_power", "defense_power", "durability", "sell_price", "rarity_tier"]
        corr_matrix = df_filtered[corr_cols].corr()
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="Viridis",
            title="Matriz de Correlación Numérica",
            template="plotly_dark"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    st.subheader("📋 Explorador de Datos de Hyrule")
    st.dataframe(
        df_filtered[["item_id", "item_name", "category", "subcategory", "attack_power", "defense_power", "durability", "sell_price", "rarity_tier", "origin_region"]],
        use_container_width=True,
        height=300
    )

# ==============================================================================
# PÁGINA 2: SEGMENTACIÓN MEDIANTE K-MEANS
# ==============================================================================
else:
    st.header("🎯 Página 2: Segmentación y Agrupamiento mediante K-Means")
    st.markdown("Visualización e interpretación de los 4 clústeres arquetípicos descubiertos por el algoritmo de aprendizaje no supervisado K-Means.")

    # 1. Gráfica con la distribución de registros por clúster (Requerimiento)
    # 2. Gráfica de dispersión para visualizar los agrupamientos (Requerimiento)
    col_dist, col_scat = st.columns([1, 2])

    with col_dist:
        st.subheader("🥧 Distribución de Registros por Clúster")
        cluster_dist = df_filtered["Cluster_Nombre"].value_counts().reset_index()
        cluster_dist.columns = ["Clúster", "Cantidad"]
        fig_donut = px.pie(
            cluster_dist,
            names="Clúster",
            values="Cantidad",
            color="Clúster",
            color_discrete_map=CLUSTER_COLORS,
            hole=0.45,
            title="Proporción del Catálogo de Hyrule",
            template="plotly_dark"
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_scat:
        st.subheader("🌌 Visualización de Clústeres (Proyección PCA 2D)")
        fig_pca = px.scatter(
            df_filtered,
            x="pca_x",
            y="pca_y",
            color="Cluster_Nombre",
            color_discrete_map=CLUSTER_COLORS,
            hover_name="item_name",
            hover_data=["category", "attack_power", "defense_power", "durability", "sell_price"],
            title="Espacio de Características Reducido (70.8% Varianza Explicada)",
            labels={"pca_x": "Componente Principal 1 (Ataque y Daño)", "pca_y": "Componente Principal 2 (Defensa y Precio)"},
            template="plotly_dark",
            opacity=0.85
        )
        st.plotly_chart(fig_pca, use_container_width=True)

    # DOS GRÁFICAS ADICIONALES PARA COMPARAR CARACTERÍSTICAS (Requerimiento Parte 6)
    st.subheader("📈 Comparación Detallada de Características por Clúster")
    g_add1, g_add2 = st.columns(2)

    with g_add1:
        st.markdown("**Gráfica Adicional 1: Boxplot de Poder de Ataque por Clúster**")
        fig_box_atk = px.box(
            df_filtered,
            x="Cluster_Nombre",
            y="attack_power",
            color="Cluster_Nombre",
            color_discrete_map=CLUSTER_COLORS,
            points="outliers",
            title="Potencial Ofensivo en cada Segmento",
            labels={"Cluster_Nombre": "Clúster", "attack_power": "Poder de Ataque"},
            template="plotly_dark"
        )
        fig_box_atk.update_layout(showlegend=False, xaxis_tickangle=-15)
        st.plotly_chart(fig_box_atk, use_container_width=True)

    with g_add2:
        st.markdown("**Gráfica Adicional 2: Dispersión Ataque vs Precio en Rupias**")
        fig_atk_price = px.scatter(
            df_filtered,
            x="attack_power",
            y="sell_price",
            color="Cluster_Nombre",
            color_discrete_map=CLUSTER_COLORS,
            hover_name="item_name",
            size="rarity_tier",
            title="Relación Daño vs Coste Comercial",
            labels={"attack_power": "Ataque", "sell_price": "Precio en Rupias (₹)"},
            template="plotly_dark"
        )
        fig_atk_price.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_atk_price, use_container_width=True)

    # TABLA CON ESTADÍSTICAS DESCRIPTIVAS DE LOS CLÚSTERES (Requerimiento Parte 6)
    st.subheader("📊 Tabla de Estadísticas Descriptivas por Clúster")
    stats_features = ["attack_power", "defense_power", "durability", "sell_price", "rarity_tier"]
    stats_df = df_filtered.groupby("Cluster_Nombre")[stats_features].agg(["mean", "median", "std"]).round(1)
    st.dataframe(stats_df, use_container_width=True)

    # SECCIÓN CON LA DESCRIPCIÓN DE LOS GRUPOS IDENTIFICADOS (Requerimiento Parte 6)
    st.subheader("🛡️ Descripción de los Grupos Identificados")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("""
        <div class='cluster-card' style='border-color: #EF4444;'>
            <h4 style='color:#EF4444; margin-top:0;'>🗡️ Clúster 1: Arsenal Ofensivo y Armas de Asalto</h4>
            <p><b>Perfil:</b> Ataque elevado (media 47.8), defensa prácticamente nula (0.7), durabilidad media (57.7) y precio accesible (571 ₹).</p>
            <p><b>Composición:</b> Espadas de una mano, mandobles, sables del desierto, lanzas y arcos de repetición. Son las herramientas de vanguardia utilizadas para infligir daño activo en combate.</p>
        </div>
        <div class='cluster-card' style='border-color: #10B981;'>
            <h4 style='color:#10B981; margin-top:0;'>🌿 Clúster 0: Recursos Básicos, Forraje y Consumibles</h4>
            <p><b>Perfil:</b> Ataque bajo (8.1), defensa baja (5.0), durabilidad reducida (33.1) y precio económico (134 ₹).</p>
            <p><b>Composición:</b> Setas, frutas, elixires, órganos de monstruos menores y comida básica. Es la base indispensable de la recolección para la supervivencia y preparación.</p>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div class='cluster-card' style='border-color: #3B82F6;'>
            <h4 style='color:#3B82F6; margin-top:0;'>🛡️ Clúster 2: Blindaje Táctico, Armaduras y Escudos</h4>
            <p><b>Perfil:</b> Ataque nulo (1.1), alta defensa (43.1), durabilidad destacada (104.7) y el precio promedio más alto de equipo común (1,433 ₹).</p>
            <p><b>Composición:</b> Escudos pesados (Escudo Hyliano, Guardián), y armaduras de Gran Hada de alta graduación. Diseñado para mitigar daño y parry.</p>
        </div>
        <div class='cluster-card' style='border-color: #F59E0B;'>
            <h4 style='color:#F59E0B; margin-top:0;'>👑 Clúster 3: Jefes Supremos, Calamidades y Reliquias Míticas</h4>
            <p><b>Perfil:</b> Máximo poder de ataque (75.7), máxima defensa (47.2) y colosal durabilidad/HP (706.2).</p>
            <p><b>Composición:</b> Lynels Plateados/Dorados, Calamity Ganon, Guardianes y armas de los Elegidos. Representan el 3.5% élite del juego y los mayores retos tácticos.</p>
        </div>
        """, unsafe_allow_html=True)

    # SECCIÓN CON LOS PRINCIPALES HALLAZGOS Y RECOMENDACIONES (Requerimiento Parte 6)
    st.subheader("💡 Principales Hallazgos y Recomendaciones Estratégicas")
    h1, h2 = st.columns(2)
    with h1:
        st.markdown("### 🔍 Hallazgos Clave")
        st.info("""
        1. **Polarización Ofensiva-Defensiva Estricta:** No existen ítems balanceados intermedios; el equipamiento se polariza radicalmente en ataque letal o blindaje protector.
        2. **Economía del Blindaje de Alto Costo:** Las piezas de defensa cuestan casi 3 veces más que las armas ofensivas debido al valor persistente de la protección en Hyrule.
        3. **Aislamiento de Entidades de Calamidad:** Las entidades del Clúster 3 tienen 12 veces más durabilidad/resistencia que el resto, requiriendo estrategias combinadas de preparación previa.
        """)

    with h2:
        st.markdown("### 🎯 Recomendaciones de Juego y Balance")
        st.success("""
        1. **Para Jugadores:** Configurar el inventario con proporción 60% Armas de Asalto (Clúster 1), 25% Blindaje (Clúster 2) y 15% Consumibles potenciados (Clúster 0).
        2. **Para Game Designers:** Introducir espadas legendarias con mayor valor comercial (>1,500 ₹) para equilibrar la economía frente a las armaduras de Gran Hada.
        3. **Curva de Dificultad:** Desarrollar una subcategoría de "Mini-Bosses" con durabilidades intermedias (200-350 HP) para suavizar el escalón hacia los Jefes Supremos.
        """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B; font-size: 0.85rem;'>Proyecto Integrador de Minería de Datos | Segmentación K-Means | The Legend of Zelda Universe</p>", unsafe_allow_html=True)
