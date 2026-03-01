# Análisis y Dashbaord de Sismicidad en Colombia (Acosta & Camargo)

Este proyecto es un análisis integral de la sismicidad en Colombia (2010 - 2026) utilizando técnicas de aprendizaje no supervisado (K-Means Clustering) para identificar patrones tectónicos y crear un panel de visualización interactivo.

## 🚀 Lo que hemos logrado

A lo largo de este proyecto, hemos desarrollado una solución de extremo a extremo para el análisis sísmico:

1. **Recopilación y Limpieza de Datos:** 
   - Extracción de datos geoespaciales y sísmicos directamente desde la API del USGS.
   - Filtrado inteligente de "microrruido" sísmico (sismos de muy baja magnitud que ensucian visualmente los patrones tectónicos), quedándonos con **2,971 eventos sísmicos significativos**. Esta decisión metodológica permite que los algoritmos de clustering identifiquen de manera mucho más nítida las estructuras geológicas principales (como los nidos sísmicos y las fallas superficiales).

2. **Modelado Avanzado (Clustering K-Means):**
   - Estandarización de variables clave (Latitud, Longitud, Profundidad).
   - Aplicación de K-Means con $K=5$, una elección justificada tanto por el Método del Codo y la métrica Silhouette, como por la coherencia geológica del país (separando claramente, por ejemplo, el Nido de Bucaramanga de las zonas de subducción del Pacífico).

3. **Notebook de Experimentación (`taller1.ipynb`):**
   - Un pipeline completo en Jupyter Notebook que guía a través del Análisis Exploratorio de Datos (EDA), Preparación, Modelado y Evaluación.
   - Incluye mapeo dinámico e inteligente que nombra los clústeres no por su ID algorítmico, sino por sus características espaciales y de profundidad reales.
   - **Parámetros Clave y Preguntas Abordadas:**
     1.  ¿Cuáles son los principales patrones de sismicidad en Colombia?
     2.  ¿Cuántos grupos (K) son óptimos para Colombia?
     3.  ¿Cómo se interpreta esto a nivel de vulnerabilidad por región?

> **Nota sobre la Transparencia y Preprocesamiento de Datos:**
> El análisis se basa en la base de datos oficial de **2,971 registros** (disponible vía Supabase). Todo el proceso es ahora completamente transparente y reproducible:
> 1. **Fuente Única**: Se consumen los datos crudos directamente de la URL oficial para evitar inconsistencias locales.
> 2. **Normalización Estricta (Mw)**: Antes de cualquier agrupación o cálculo estadístico, se normalizó la magnitud de todos los eventos a la escala de Magnitud de Momento (**Mw**). Esto asegura que el clustering y las comparativas regionales sean válidas y comparables.
> 3. **Consistencia Total**: Todas las visualizaciones, incluyendo los gráficos de codo/silueta ($K=5$) y las tablas de perfilamiento de la Pestaña 3, están sincronizadas con este dataset limpio y normalizado.

---
4. **Dashboard Interactivo (`dashboard.py`):**
   - Una aplicación web en Streamlit rica en interactividad.
   - **Estructura Tridimensional:** Un mapa 3D que permite visualizar la profundidad real de los nidos sísmicos (como la inmersión de la placa de Nazca bajo la placa Sudamericana).
   - **Diagnóstico Regional (Snake Plot):** Gráficos avanzados para comparar perfiles y métricas sísmicas entre las diferentes zonas identificadas.
   - **Presupuesto y Contexto Institucional:** Comparativas de presupuesto (2025) entre el SGC (Servicio Geológico Colombiano) y la UNGRD.

## 📁 Estructura del Proyecto

- `dashboard.py`: Aplicación principal de Streamlit.
- `taller1.ipynb`: Notebook con el proceso analítico paso a paso.
- `reporte.md`: Reporte ejecutivo con hallazgos clave, interpretaciones geológicas y justificaciones metodológicas.
- `data/`: Directorio que contiene los datos descargados, procesados y los perfiles de los clústeres (`clustered_data.csv`, `cluster_profile.csv`).

## 🛠️ Cómo Ejecutar el Dashboard (¡Fácil y Automático!)

Para asegurar que cualquier persona (como el profesor) pueda ejecutar el proyecto sin problemas de dependencias o rutas, hemos creado scripts que automáticamente crean un entorno virtual (`venv`), instalan las librerías necesarias de `requirements.txt` y corren el dashboard.

**Si usas Windows:**
1. Da doble clic en el archivo `iniciar_proyecto.bat` que se encuentra en la carpeta.
   *(Alternativamente, abre una terminal en esta carpeta y ejecuta `iniciar_proyecto.bat`)*

**Si usas Mac / Linux:**
1. Abre una terminal en esta carpeta.
2. Dale permisos de ejecución al script si es necesario: `chmod +x iniciar_proyecto.sh`
3. Ejecuta el script: `./iniciar_proyecto.sh`

> **⚠️ Nota importante para el envío:** Al momento de comprimir y enviar la carpeta del proyecto, **NO** incluyas la carpeta `venv`. Los entornos virtuales están ligados a las rutas del computador donde se crearon y causarán errores si se envían. El profesor debe generar el suyo propio al ejecutar el script `iniciar_proyecto`.
