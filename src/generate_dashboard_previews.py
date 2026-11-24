"""
Genera capturas visuales de alta fidelidad del Dashboard Formal con Difuminados (Página 1 y Página 2)
para ser incorporadas en el reporte oficial en PDF (Parte 7).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

# Cargar datos procesados
df = pd.read_csv("data/zelda_hyrule_compendium_procesado.csv")

# 1. GENERAR CAPTURA PÁGINA 1: ANÁLISIS GENERAL
fig = plt.figure(figsize=(15, 9.5), facecolor="#0f172a")

# Barra lateral simulada
ax_side = fig.add_axes([0.02, 0.05, 0.20, 0.90], facecolor="#1e293b")
ax_side.axis("off")
ax_side.text(0.08, 0.94, "Panel de Control", color="#38BDF8", fontsize=13, weight="bold")
ax_side.text(0.08, 0.88, "Navegacion:", color="#94A3B8", fontsize=10, weight="bold")
ax_side.text(0.08, 0.84, "[x] Analisis General", color="#38BDF8", fontsize=10, weight="bold")
ax_side.text(0.08, 0.80, "[ ] Segmentacion K-Means", color="#94A3B8", fontsize=10)
ax_side.text(0.08, 0.72, "Filtros Multivariados:", color="#E2E8F0", fontsize=11, weight="bold")
ax_side.text(0.08, 0.67, "Cluster: 4 seleccionados", color="#94A3B8", fontsize=9)
ax_side.text(0.08, 0.60, "Categoria: 7 seleccionadas", color="#94A3B8", fontsize=9)
ax_side.text(0.08, 0.52, "Precio: 0 a 5,000 Rupias", color="#94A3B8", fontsize=9)
ax_side.text(0.08, 0.44, "Rareza: Tier 1 a 5", color="#94A3B8", fontsize=9)

# Área principal
ax_main = fig.add_axes([0.25, 0.05, 0.73, 0.90], facecolor="#0f172a")
ax_main.axis("off")

# Título y subtítulo
ax_main.text(0.0, 0.96, "Hyrule Data Insights", color="#F8FAFC", fontsize=17, weight="bold")
ax_main.text(0.0, 0.92, "Pagina 1: Analisis General del Compendio Multivariado", color="#94A3B8", fontsize=11)

# KPI Cards en Página 1
kpis = [
    ("TOTAL OBSERVACIONES", "947 / 947", "#F8FAFC"),
    ("PODER OFENSIVO MEDIO", "27.7 pts", "#60A5FA"),
    ("DURABILIDAD MEDIANA", "40.0 pts", "#34D399"),
    ("VALORACION PROMEDIO", "535 Rupias", "#FBBF24")
]
for i, (title, val, col) in enumerate(kpis):
    x0 = 0.0 + i * 0.25
    rect = patches.FancyBboxPatch((x0, 0.81), 0.23, 0.08, boxstyle="round,pad=0.01", facecolor="#1e293b", edgecolor="#334155", linewidth=1.0)
    ax_main.add_patch(rect)
    ax_main.text(x0 + 0.115, 0.86, title, color="#94A3B8", fontsize=7.5, weight="bold", ha="center")
    ax_main.text(x0 + 0.115, 0.825, val, color=col, fontsize=11, weight="bold", ha="center")

# Gráfica 1: Histograma de Ataque
ax_g1 = fig.add_axes([0.26, 0.46, 0.33, 0.28], facecolor="#1e293b")
ax_g1.tick_params(colors="#94A3B8", labelsize=8)
for spine in ax_g1.spines.values():
    spine.set_color("#334155")
df["attack_power"].plot(kind="hist", bins=20, ax=ax_g1, color="#2563EB", alpha=0.85)
ax_g1.set_title("Distribucion de Poder Ofensivo", color="#F8FAFC", fontsize=10, weight="bold")
ax_g1.set_xlabel("Poder de Ataque (Puntos)", color="#94A3B8", fontsize=8)
ax_g1.set_ylabel("Frecuencia", color="#94A3B8", fontsize=8)

# Gráfica 2: Dispersión Durabilidad vs Precio
ax_g2 = fig.add_axes([0.63, 0.46, 0.33, 0.28], facecolor="#1e293b")
ax_g2.tick_params(colors="#94A3B8", labelsize=8)
for spine in ax_g2.spines.values():
    spine.set_color("#334155")
ax_g2.scatter(df["durability"], df["sell_price"], c=df["rarity_tier"], cmap="Blues", alpha=0.8, s=22)
ax_g2.set_title("Durabilidad vs Precio en Rupias", color="#F8FAFC", fontsize=10, weight="bold")
ax_g2.set_xlabel("Durabilidad / HP", color="#94A3B8", fontsize=8)
ax_g2.set_ylabel("Precio (Rupias)", color="#94A3B8", fontsize=8)

# Gráfica 3: Recursos por Región
ax_g3 = fig.add_axes([0.26, 0.10, 0.33, 0.28], facecolor="#1e293b")
ax_g3.tick_params(colors="#94A3B8", labelsize=7)
for spine in ax_g3.spines.values():
    spine.set_color("#334155")
reg_counts = df["origin_region"].value_counts().head(7)
reg_counts.plot(kind="barh", ax=ax_g3, color="#059669", alpha=0.85)
ax_g3.set_title("Abundancia por Region", color="#F8FAFC", fontsize=10, weight="bold")
ax_g3.set_xlabel("Cantidad", color="#94A3B8", fontsize=8)

# Gráfica 4: Matriz de Correlación
ax_g4 = fig.add_axes([0.63, 0.10, 0.33, 0.28], facecolor="#1e293b")
ax_g4.tick_params(colors="#94A3B8", labelsize=7)
for spine in ax_g4.spines.values():
    spine.set_color("#334155")
cols_c = ["attack_power", "defense_power", "durability", "sell_price", "rarity_tier"]
im = ax_g4.imshow(df[cols_c].corr(), cmap="Blues")
ax_g4.set_xticks(range(len(cols_c)))
ax_g4.set_yticks(range(len(cols_c)))
ax_g4.set_xticklabels(["Atk", "Def", "Dur", "Prc", "Rar"], color="#94A3B8", fontsize=7)
ax_g4.set_yticklabels(["Atk", "Def", "Dur", "Prc", "Rar"], color="#94A3B8", fontsize=7)
ax_g4.set_title("Matriz de Correlacion Numerica", color="#F8FAFC", fontsize=10, weight="bold")

plt.savefig("assets/dashboard_screenshot_page1.png", dpi=250, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print("Captura formal de Página 1 generada: assets/dashboard_screenshot_page1.png")

# 2. GENERAR CAPTURA PÁGINA 2: SEGMENTACIÓN K-MEANS
fig2 = plt.figure(figsize=(15, 9.5), facecolor="#0f172a")

# Barra lateral simulada
ax_side2 = fig2.add_axes([0.02, 0.05, 0.20, 0.90], facecolor="#1e293b")
ax_side2.axis("off")
ax_side2.text(0.08, 0.94, "Panel de Control", color="#38BDF8", fontsize=13, weight="bold")
ax_side2.text(0.08, 0.88, "Navegacion:", color="#94A3B8", fontsize=10, weight="bold")
ax_side2.text(0.08, 0.84, "[ ] Analisis General", color="#94A3B8", fontsize=10)
ax_side2.text(0.08, 0.80, "[x] Segmentacion K-Means", color="#38BDF8", fontsize=10, weight="bold")
ax_side2.text(0.08, 0.72, "Filtros Multivariados:", color="#E2E8F0", fontsize=11, weight="bold")
ax_side2.text(0.08, 0.67, "Cluster: 4 seleccionados", color="#94A3B8", fontsize=9)
ax_side2.text(0.08, 0.60, "Categoria: 7 seleccionadas", color="#94A3B8", fontsize=9)
ax_side2.text(0.08, 0.52, "Precio: 0 a 5,000 Rupias", color="#94A3B8", fontsize=9)
ax_side2.text(0.08, 0.44, "Rareza: Tier 1 a 5", color="#94A3B8", fontsize=9)

# Área principal
ax_main2 = fig2.add_axes([0.25, 0.05, 0.73, 0.90], facecolor="#0f172a")
ax_main2.axis("off")

# Título y subtítulo
ax_main2.text(0.0, 0.96, "Hyrule Data Insights", color="#F8FAFC", fontsize=17, weight="bold")
ax_main2.text(0.0, 0.92, "Pagina 2: Segmentacion y Clusteres K-Means (K=4)", color="#94A3B8", fontsize=11)

# KPI Cards en Página 2
for i, (title, val, col) in enumerate(kpis):
    x0 = 0.0 + i * 0.25
    rect = patches.FancyBboxPatch((x0, 0.81), 0.23, 0.08, boxstyle="round,pad=0.01", facecolor="#1e293b", edgecolor="#334155", linewidth=1.0)
    ax_main2.add_patch(rect)
    ax_main2.text(x0 + 0.115, 0.86, title, color="#94A3B8", fontsize=7.5, weight="bold", ha="center")
    ax_main2.text(x0 + 0.115, 0.825, val, color=col, fontsize=11, weight="bold", ha="center")

# Gráfica 1: Distribución circular de registros por clúster
ax_pie = fig2.add_axes([0.26, 0.48, 0.28, 0.27], facecolor="#1e293b")
counts = df["Cluster_Nombre"].value_counts()
formal_colors = ["#E11D48", "#059669", "#2563EB", "#D97706"]
ax_pie.pie(counts, labels=None, autopct="%1.1f%%", colors=formal_colors, pctdistance=0.72, textprops={'color': "white", 'fontsize': 8, 'weight': 'bold'}, wedgeprops=dict(width=0.45, edgecolor='#1e293b'))
ax_pie.set_title("Proporcion por Cluster", color="#F8FAFC", fontsize=10, weight="bold")

# Gráfica 2: Dispersión PCA 2D
ax_scat = fig2.add_axes([0.58, 0.48, 0.38, 0.27], facecolor="#1e293b")
ax_scat.tick_params(colors="#94A3B8", labelsize=8)
for spine in ax_scat.spines.values():
    spine.set_color("#334155")
cluster_cmap = {
    "Arsenal Ofensivo y Armas de Asalto": "#E11D48",
    "Recursos Básicos, Forraje y Consumibles": "#059669",
    "Blindaje Táctico, Armaduras y Escudos": "#2563EB",
    "Jefes Supremos, Calamidades y Reliquias Míticas": "#D97706"
}
point_colors = df["Cluster_Nombre"].map(cluster_cmap)
ax_scat.scatter(df["pca_x"], df["pca_y"], c=point_colors, alpha=0.85, s=26, edgecolor="none")
ax_scat.set_title("Proyeccion de Clusteres (PCA 2D)", color="#F8FAFC", fontsize=10, weight="bold")
ax_scat.set_xlabel("Componente Principal 1", color="#94A3B8", fontsize=8)
ax_scat.set_ylabel("Componente Principal 2", color="#94A3B8", fontsize=8)

# Gráfica Adicional 1: Boxplot de Ataque por Clúster
ax_box = fig2.add_axes([0.26, 0.12, 0.32, 0.26], facecolor="#1e293b")
ax_box.tick_params(colors="#94A3B8", labelsize=7)
for spine in ax_box.spines.values():
    spine.set_color("#334155")
df_box_data = [df[df["Cluster_Nombre"] == name]["attack_power"].values for name in counts.index]
bplot = ax_box.boxplot(df_box_data, patch_artist=True, tick_labels=["Arsenal", "Recursos", "Blindaje", "Jefes"])
for patch, color in zip(bplot['boxes'], formal_colors):
    patch.set_facecolor(color)
ax_box.set_title("Poder Ofensivo por Cluster", color="#F8FAFC", fontsize=10, weight="bold")
ax_box.set_ylabel("Poder de Ataque", color="#94A3B8", fontsize=8)

# Gráfica Adicional 2: Ataque vs Precio
ax_ap = fig2.add_axes([0.62, 0.12, 0.34, 0.26], facecolor="#1e293b")
ax_ap.tick_params(colors="#94A3B8", labelsize=8)
for spine in ax_ap.spines.values():
    spine.set_color("#334155")
ax_ap.scatter(df["attack_power"], df["sell_price"], c=point_colors, alpha=0.75, s=20)
ax_ap.set_title("Ataque vs Precio en Rupias", color="#F8FAFC", fontsize=10, weight="bold")
ax_ap.set_xlabel("Poder de Ataque", color="#94A3B8", fontsize=8)
ax_ap.set_ylabel("Precio (Rupias)", color="#94A3B8", fontsize=8)

plt.savefig("assets/dashboard_screenshot_page2.png", dpi=250, facecolor=fig2.get_facecolor(), edgecolor="none")
plt.close()
print("Captura formal de Página 2 generada: assets/dashboard_screenshot_page2.png")
