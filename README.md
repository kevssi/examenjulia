# Ventas del Formato Físico y Digital de los Videojuegos mediante K-Means

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-orange.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 1. Descripción del Proyecto
Este proyecto desarrolla una solución completa de **Minería de Datos y Aprendizaje Automático No Supervisado** aplicando el algoritmo **K-Means** sobre el mercado de videojuegos globales. Analiza el comportamiento de más de 900 títulos entre ventas físicas (discos/cartuchos) y descargas digitales para optimizar inventarios y estrategias de comercialización.

El proyecto cuenta con:
* Dataset original con anomalías controladas y dataset procesado normalizado.
* Pipeline en Python con evaluación de $K$ (Método del Codo y Silueta), PCA 2D y caracterización de centroides.
* Notebook interactivo en Jupyter (`notebooks/proyecto_kmeans_videojuegos.ipynb`).
* Dashboard interactivo en Streamlit con diseño formal, difuminados, 4 KPIs y 5 filtros en tiempo real.
* Documentación oficial completa en PDF que cubre los 8 apartados de la rúbrica.

---

## 2. Problemática Analizada
El riesgo financiero y de inventario estancado en tiendas y distribuidoras por desconocer qué títulos tienen alta tracción comercial, cuáles son fracasos y en qué canal (físico o digital) se desempeñan mejor. El modelo segmenta el catálogo para determinar a qué juegos fabricarles copias físicas y a cuáles vender exclusivamente por internet para ahorrar costos de manufactura y distribución.

---

## 3. Clústeres Descubiertos ($K=4$)

| Clúster | Nombre Asignado | Venta Física Media | Venta Digital Media | Precio Medio | Calificación Media | Horas Media | Proporción | Estrategia de Negocio |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | **Superventas Globales (Blockbusters)** | 8.69 M | 12.39 M | $69.99 | 87.7 pts | 46.4 h | 18.4% (169 juegos) | Máxima prioridad de stock físico y publicidad masiva. |
| **1** | **Fracasos Comerciales y Bajo Rendimiento** | 0.41 M | 0.57 M | $55.97 | 52.7 pts | 17.4 h | 24.3% (224 juegos) | No fabricar más discos; aplicar descuentos rápidos de liquidación. |
| **2** | **Coleccionables de Consola (Físico Fuerte)** | 6.65 M | 2.87 M | $61.28 | 84.1 pts | 35.8 h | 22.8% (210 juegos) | Priorizar estanterías físicas y ediciones especiales de colección. |
| **3** | **Éxitos Digitales e Indies Virales** | 0.60 M | 7.71 M | $35.01 | 81.7 pts | 30.3 h | 34.5% (317 juegos) | **Venta 100% digital**; cero gasto en cajas ni fletes de transporte. |

---

## 4. Estructura del Repositorio

```text
exameeen/
│
├── data/                                              # Datasets del proyecto
│   ├── videojuegos_ventas_original.csv               # Dataset con 928 filas y anomalías controladas (Parte 2)
│   └── videojuegos_ventas_procesado.csv              # Dataset limpio con 920 filas y clústeres (Parte 3 y 4)
│
├── notebooks/                                         # Entorno interactivo Jupyter
│   └── proyecto_kmeans_videojuegos.ipynb             # Notebook con todas las celdas ejecutadas (Partes 1 a 5)
│
├── src/                                               # Código fuente modular
│   ├── generate_dataset_videojuegos.py               # Generador del dataset con ruido controlado
│   ├── process_kmeans_videojuegos.py                 # Pipeline de limpieza, evaluación de K y K-Means
│   ├── build_official_documentation_pdf.py           # Generador del reporte PDF oficial de 8 apartados (Parte 7)
│   └── build_rubric_answers_pdf.py                   # Generador del desglose detallado de la rúbrica
│
├── dashboard/                                         # Dashboard interactivo
│   └── app.py                                         # Aplicación en Streamlit (Páginas 1 y 2 con filtros)
│
├── docs/                                              # Documentos oficiales de entrega
│   ├── Documentacion_Oficial_Proyecto_KMeans_Videojuegos.pdf  # Documentación formal de 8 apartados (Parte 7)
│   └── Respuestas_Rubrica_Detallada_Proyecto.pdf      # Respuestas punto por punto a las Partes 1 a 8
│
└── assets/                                            # Gráficas generadas para los reportes
    └── reporte_videojuegos/
        ├── 1_heatmap_correlacion.png
        ├── 2_codo_silueta.png
        ├── 3_pca_clusters.png
        ├── 4_boxplot_ventas.png
        └── 5_dona_proporcion.png
```

---

## 5. Instrucciones de Instalación y Ejecución

### Requisitos Previos
* Python 3.11 o superior instalado.

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar el Pipeline de Minería de Datos
```bash
python src/process_kmeans_videojuegos.py
```

### Ejecutar el Dashboard Interactivo
```bash
streamlit run dashboard/app.py
```
El dashboard se abrirá automáticamente en tu navegador web en: `http://localhost:8501`.
