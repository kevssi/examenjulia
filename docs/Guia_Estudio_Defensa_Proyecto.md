# 📘 Guía de Estudio y Defensa de Proyecto: Minería de Datos y K-Means

**Proyecto:** Segmentación de Datos mediante K-Means y Desarrollo de un Dashboard Interactivo  
**Caso de Estudio:** The Legend of Zelda: Hyrule Compendium  
**Herramientas:** Python, Scikit-learn, Pandas, Streamlit, Matplotlib, Seaborn  

---

## 1. ¿Qué es este proyecto?

Es un proyecto de **Minería de Datos y Aprendizaje Automático No Supervisado (Unsupervised Machine Learning)**.

A diferencia del aprendizaje supervisado (donde los datos ya vienen con una etiqueta o respuesta correcta predefinida), en este proyecto tomamos un catálogo de **más de 900 objetos y entidades de *The Legend of Zelda*** con múltiples estadísticas numéricas (ataque, defensa, durabilidad, precio y rareza) y dejamos que un algoritmo matemático (**K-Means**) encuentre de forma autónoma los **patrones ocultos y grupos naturales (arquetipos tácticos)** que existen en el juego.

---

## 2. ¿Para qué sirve?

Sirve para dos propósitos fundamentales:

1. **En la Industria de Videojuegos (Game Data Science & Balance):**
   - Permite a los diseñadores de juego (*Game Designers*) auditar la economía y la curva de poder de los objetos.
   - Identifica si existen armas sobrevaloradas (*overpowered*) o infravaloradas.
   - Detecta asimetrías: por ejemplo, descubrimos que los objetos defensivos cuestan casi el triple en rupias que las armas de ataque debido a su durabilidad permanente.

2. **Para el Usuario / Jugador:**
   - Facilita la toma de decisiones estratégicas de inventario: saber qué armas guardar para daño directo, qué equipo reservar para mitigación pasiva y cómo gestionar recursos de sustento antes de enfrentar jefes colosales.

---

## 3. ¿Qué contiene el proyecto?

El proyecto está estructurado formalmente en **8 partes** y contiene:

1. **Dataset Original (`data/zelda_hyrule_compendium_original.csv`):**
   - 954 registros y 12 variables (identificadores, nombres, categorías, regiones y estadísticas).
   - Contiene imperfecciones controladas (7 duplicados, valores nulos y anomalías con números negativos) para demostrar capacidad de auditoría y limpieza de datos.

2. **Pipeline de Limpieza y Procesamiento (`src/process_kmeans.py` / `src/analisis_kmeans.py`):**
   - Normalización de texto y eliminación de duplicados (quedando 947 filas limpias).
   - Imputación contextual de valores nulos utilizando la mediana de cada categoría.
   - Corrección de datos anómalos.
   - Estandarización de variables con `StandardScaler`.

3. **Modelo Matemático K-Means:**
   - Evaluación rigurosa de 7 valores de $K$ (de 2 a 8).
   - Gráfica del Método del Codo (SSE) y Coeficiente de Silueta.
   - Selección justificada de $K=4$ clústeres.
   - Comparación formal de dos configuraciones ($K=4$ vs $K=3$).
   - Reducción de dimensionalidad con PCA (2 componentes explicando el 70.8% de la varianza total).

4. **Dataset Procesado (`data/zelda_hyrule_compendium_procesado.csv`):**
   - Archivo con todas las variables limpias y las columnas añadidas: `Cluster`, `Cluster_Nombre`, `pca_x` y `pca_y`.

5. **Jupyter Notebook Oficial (`notebooks/proyecto_kmeans_zelda.ipynb`):**
   - Cuaderno interactivo con celdas ejecutadas, código fuente, explicaciones en Markdown y gráficos integrados (Partes 1 a 5).

6. **Dashboard Interactivo Web (`dashboard/app.py`):**
   - Aplicación en Streamlit con diseño formal, difuminados *glassmorphism* e iconografía Lucide.
   - Dos páginas independientes: *Página 1: Análisis General* y *Página 2: Segmentación K-Means*.
   - 4 tarjetas KPI en tiempo real, 4 gráficos analíticos interactivos y 3 filtros dinámicos funcionales.

7. **Documento de Reporte en PDF (`docs/Reporte_Proyecto_Integrador_KMeans_Zelda.pdf`):**
   - Informe académico formal de 8 páginas que cubre con exactitud los 8 apartados requeridos.

8. **Repositorio Git y Documentación (`README.md`):**
   - Estructura limpia de carpetas con control de versiones y dependencias en `requirements.txt`.

---

## 4. Conceptos Teóricos Clave (Lo que la Maestra va a Preguntar)

### ¿Cómo funciona el algoritmo K-Means?
K-Means es un algoritmo de agrupamiento particional basado en centroides:
1. **Inicialización:** Selecciona $K$ puntos iniciales como centroides (utilizamos `k-means++` para que los centroides iniciales estén distanciados entre sí).
2. **Asignación:** Asigna cada observación al centroide más cercano utilizando la **Distancia Euclidiana**:
   $$d(p, q) = \sqrt{\sum_{i=1}^{n} (p_i - q_i)^2}$$
3. **Actualización:** Recalcula la posición de cada centroide como el promedio (media matemática) de todos los puntos asignados a ese grupo.
4. **Convergencia:** Repite los pasos 2 y 3 hasta que los centroides ya no se muevan o se alcance el número máximo de iteraciones.

### ¿Por qué fue obligatorio usar `StandardScaler`? (Pregunta Trampa Típica)
- **Pregunta de la maestra:** *"¿Qué pasaría si ejecutan K-Means sin estandarizar?"*
- **Respuesta ganadora:**  
  *El cálculo de distancias euclidianas depende directamente de la escala de los números. En nuestro dataset, el precio (`sell_price`) llega hasta 5,000 rupias y la durabilidad a 1,000, mientras que el nivel de rareza (`rarity_tier`) va del 1 al 5 y la defensa de 0 a 100. Si no hubiéramos estandarizado con `StandardScaler`, la variable precio habría dominado el 99% de la distancia matemática, ignorando la rareza y el ataque. `StandardScaler` transforma todas las variables a media $\mu = 0$ y desviación estándar $\sigma = 1$ (Z-Score), otorgándoles el mismo peso geométrico.*

### ¿Cómo determinaron que $K=4$ era el número óptimo de clústeres?
Utilizamos dos criterios combinados:
1. **El Método del Codo (Elbow Method):** Graficamos la Inercia (la suma de errores cuadráticos intra-clúster, SSE). A partir de $K=4$, la curva sufre un cambio de pendiente evidente y la ganancia de compactación se estabiliza.
2. **El Coeficiente de Silueta:** Mide qué tan similar es un objeto a su propio clúster (cohesión) comparado con los demás clústeres (separación). En $K=4$ obtuvimos una silueta sólida de **0.3959**, con un índice Calinski-Harabasz de **479.7** y Davies-Bouldin de **0.9452**.
3. **Sentido de Negocio / Dominio:** $K=4$ separa a la perfección los 4 arquetipos tácticos de Hyrule (Ataque, Defensa, Recursos y Jefes de Calamidad).

### ¿Para qué sirvió PCA (Principal Component Analysis)?
Nuestros datos tienen **5 dimensiones** (`attack_power`, `defense_power`, `durability`, `sell_price`, `rarity_tier`). Los seres humanos no podemos visualizar un gráfico de 5 dimensiones. PCA aplicó una transformación ortogonal lineal para reducir esas 5 variables a **2 Componentes Principales (`pca_x`, `pca_y`)**, reteniendo el **70.8% de la información (varianza total)** y permitiéndonos graficar los clústeres en un plano cartesiano 2D.

---

## 5. Los 4 Clústeres de Hyrule (De Memoria)

| Clúster | Denominación Oficial | Cantidad | Características Promedio | ¿Qué ítems contiene? |
| :---: | :--- | :---: | :--- | :--- |
| **0** | **Recursos Básicos, Forraje y Consumibles** | 344 (36.3%) | Ataque: 8.1 \| Defensa: 5.0 \| Durabilidad: 33.1 \| Precio: 134 Rupias | Setas, frutas, elixires, recetas de comida y botín menor. |
| **1** | **Arsenal Ofensivo y Armas de Asalto** | 432 (45.6%) | Ataque: 47.8 \| Defensa: 0.7 \| Durabilidad: 57.7 \| Precio: 571 Rupias | Espadas, mandobles, sables del desierto, lanzas y arcos. |
| **2** | **Blindaje Táctico, Armaduras y Escudos** | 138 (14.6%) | Ataque: 1.1 \| Defensa: 43.1 \| Durabilidad: 104.7 \| Precio: 1,433 Rupias | Escudos pesados (Hyliano, Guardián) y armaduras de Gran Hada. |
| **3** | **Jefes Supremos, Calamidades y Reliquias Míticas** | 33 (3.5%) | Ataque: 75.7 \| Defensa: 47.2 \| Durabilidad: 706.2 \| Precio: 1,318 Rupias | Calamity Ganon, Lynels Dorados/Plateados y equipo legendario. |

---

## 6. Simulador de Preguntas de la Maestra (Pregunta -> Respuesta Rápida)

#### P1: ¿Por qué eligieron K-Means y no otro algoritmo como Regresión o Clasificación?
> **Respuesta:** Porque nuestro problema no tenía etiquetas previas (nadie le había dicho a los datos qué objeto pertenecía a qué grupo). Necesitábamos una técnica **no supervisada** para descubrir la estructura natural de los datos por similitud de características.

#### P2: ¿Qué variables utilizaron para entrenar el modelo y por qué?
> **Respuesta:** Seleccionamos 5 variables numéricas: `attack_power` (daño), `defense_power` (mitigación), `durability` (resistencia), `sell_price` (economía en rupias) y `rarity_tier` (jerarquía de 1 a 5). Esta combinación cubre de manera equilibrada la dimensión ofensiva, defensiva, económica y de prestigio.

#### P3: ¿Cómo limpiaron los datos antes de entrenar?
> **Respuesta:** 
> 1. Eliminamos 7 registros duplicados exactos (.drop_duplicates()).
> 2. Normalizamos cadenas de texto (.strip() y capitalización consistente).
> 3. Detectamos y corregimos anomalías de valores negativos en precio y durabilidad convirtiéndolos a valores positivos absolutos.
> 4. Imputamos valores nulos utilizando la mediana estadística agrupada por categoría para no alterar la distribución de los datos.

#### P4: ¿Qué diferencia encontraron al comparar dos configuraciones de K?
> **Respuesta:** Comparamos $K=4$ frente a $K=3$. Con $K=3$ la inercia fue mucho mayor (2,503 vs 1,874) y la silueta cayó a 0.3553. Lo más grave fue que $K=3$ fusionó erróneamente las piezas de blindaje defensivo con las armas de ataque en un solo grupo mixto, perdiendo la distinción táctica que en $K=4$ sí se refleja claramente.

#### P5: ¿Qué conclusiones o recomendaciones prácticas obtuvieron del análisis?
> **Respuesta:**
> 1. **Para jugadores:** No existen objetos híbridos; el juego penaliza intentar balancear y exige alternar armas ofensivas del Clúster 1 con escudos del Clúster 2.
> 2. **Para desarrolladores:** Existe una gran brecha económica: las armaduras cuestan casi el triple que las armas. Se recomienda introducir espadas legendarias más caras para equilibrar la economía de rupias.
> 3. **Para la curva de dificultad:** Los Jefes del Clúster 3 tienen 12 veces más vida útil que el resto; se sugiere crear una categoría intermedia de 'Mini-Jefes' (200-350 HP) para suavizar el aprendizaje del jugador.

#### P6: ¿Cuáles son las limitaciones de su modelo?
> **Respuesta:** 
> 1. K-Means asume clústeres esféricos de varianzas similares (podría enriquecerse con DBSCAN o Modelos de Mezclas Gaussianas).
> 2. No toma en cuenta variables espaciales de geolocalización o clima en el mapa de Hyrule.

---

## 7. Discurso de Presentación de 1 Minuto (Speech Inicial)

> *"Buenos días profesora y compañeros. Nuestro proyecto integrador consistió en la minería de datos y segmentación no supervisada del compendio de 'The Legend of Zelda', abarcando más de 900 registros entre armamento, monstruos y recursos.*  
> *Implementamos el algoritmo K-Means analizando cinco dimensiones clave: ataque, defensa, durabilidad, precio y rareza. Tras auditar y limpiar los datos, escalamos las variables con StandardScaler y evaluamos siete valores de K mediante el método del codo y el coeficiente de silueta, determinando que K=4 es la configuración óptima.*  
> *Esto nos permitió descubrir cuatro arquetipos bien definidos: Armamento de Asalto, Blindaje Táctico, Recursos Básicos y Jefes de Calamidad.*  
> *Finalmente, construimos un dashboard interactivo en Streamlit con visualizaciones analíticas, KPIs y filtros multivariados para explorar estos resultados en tiempo real, respaldado por nuestro informe formal en PDF y repositorio público en GitHub."*
