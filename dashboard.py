
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- CONTEXTO DE EJECUCIÓN ---
# El script busca los datos en la carpeta 'data/' relativa a su ubicación.

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Sismicidad en Colombia - Storytelling",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CÁLIDOS ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #333333; }
    h1, h2 { color: #008B8B !important; }
    h3 { color: #FF8C00 !important; }
    div[data-testid="stMetric"] {
        background-color: #F0F8FF;
        border-left: 55px solid #FF8C00;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_all_data():
    df = pd.read_csv('data/clustered_data.csv')
    # Handle multi-header for profile correctly
    profile = pd.read_csv('data/cluster_profile.csv', header=[0, 1], index_col=0)
    profile.columns = ['_'.join(col).strip() for col in profile.columns.values]
    
    snake = pd.read_csv('data/snake_data.csv')
    budget = pd.read_csv('data/budget_history.csv')
    # Reverting to the previous aggregated data as requested
    world_data = pd.read_csv('data/world_seismicity_2025_aggregated.csv')
    
    df['time'] = pd.to_datetime(df['time'], utc=True, format='ISO8601')
    # Add year column for animation
    df['year'] = df['time'].dt.year

    # --- Dynamic Cluster Name Assignment (Replicated from Notebook) ---
    # This assumes 'cluster', 'latitude', 'longitude', 'depth' are in clustered_data.csv
    dynamic_cluster_names = {}
    if 'cluster' in df.columns and 'latitude' in df.columns and 'depth' in df.columns:
        means = df.groupby('cluster')[["latitude", "depth"]].mean()
        

        for idx, row in means.iterrows():
            lat, depth = row["latitude"], row["depth"]
            if depth > 100:
                if lat > 0: dynamic_cluster_names[idx] = "Santanderes (Nido de Bucaramanga)"
                else: dynamic_cluster_names[idx] = "Sur / Ecuador (Nido Profundo)"
            else:
                if lat < 0: dynamic_cluster_names[idx] = "Pacífico Sur (Superficial)"
                elif lat > 7.5: dynamic_cluster_names[idx] = "Llanos y Piedemonte Orientales"
                else: dynamic_cluster_names[idx] = "Centro y Pacífico Norte (Superficial)"

        df["Nombre Región"] = df["cluster"].map(dynamic_cluster_names)
    else:
        # Fallback if essential columns are missing for dynamic naming
        st.warning("Warning: 'cluster', 'latitude', or 'depth' columns not found for dynamic region naming.")
        df["Nombre Región"] = df["cluster"].astype(str) # Use cluster ID as name
    # --- End Dynamic Cluster Name Assignment ---

    return df, profile, snake, budget, world_data, dynamic_cluster_names # Return dynamic_cluster_names

try:
    df, profile, snake, budget, world_data, cluster_id_to_name_map = load_all_data() # Unpack dynamic_cluster_names
except Exception as e:
    st.error(f"Error cargando datos: {e}")
    st.stop()

# --- NAVEGACIÓN ---
st.sidebar.title("🧭 Navegación")
page = st.sidebar.radio("Ir a:", ["🏠 Inicio: El Problema", "📉 Nudo: Datos y Presupuesto", "✅ Desenlace: Solución"])

# --- SECCIÓN 1: INICIO ---
if page == "🏠 Inicio: El Problema":

    st.title("Colombia: Un Territorio en Movimiento")
    
    st.write("### Sismicidad Mundial en 2025")
    st.markdown("""
    Colombia se localiza en el cinturón de fuego del pacífico, una de las zonas sísmicamente más activas del planeta. Asi mismo, se encuentra en medio en el punto de convergencia de las placas de Nazca, Caribe y Sudamérica.     
    Para entender mejor nuestra realidad, a continuación se muestra el número de sismos registrados por país en 2025 (Mag (Mw) >= 4).
    """)

    fig_world = px.choropleth(
        world_data, locations="country", locationmode="country names",
        color="earthquakes_2025", hover_name="country",
        title="Sismicidad Mundial 2025 (Eventos por País)",
        color_continuous_scale=px.colors.sequential.Reds
    )
    fig_world.update_layout(height=500)
    st.plotly_chart(fig_world, use_container_width=True)

# --- SECCIÓN 2: NUDO ---
elif page == "📉 Nudo: Datos y Presupuesto":
    st.title("El Reto del Monitoreo y Recursos")
    
    st.markdown("""
    Instituciones como el **Servicio Geológico Colombiano (SGC)** y la **Unidad Nacional De Gestion Del Riesgo (UNGRD)** deben gestionar la seguridad sísmica nacional con presupuestos finitos.""")
    
    
    # Filter for 2025 only for the specific comparison chart
    budget_2025 = budget[budget['year'] == 2025]
    
    if not budget_2025.empty:
        # Prepare data for 2025 comparison
        comp_2025 = pd.DataFrame({
            'Institución': ['SGC', 'UNGRD'],
            'Presupuesto (COP)': [budget_2025['sgc_budget'].values[0], budget_2025['ungrd_budget'].values[0]]
        })
        
        # Format the budget values as string for display if needed
        fig_comp = px.bar(comp_2025, x='Institución', y='Presupuesto (COP)', 
                         title='Comparativa de Presupuesto 2025',
                         color='Institución',
                         color_discrete_map={'SGC': '#008B8B', 'UNGRD': '#FF8C00'})
        fig_comp.update_layout(height=500, plot_bgcolor='white')
        st.plotly_chart(fig_comp, use_container_width=True)

# --- SECCIÓN 3: DESENLACE ---
elif page == "✅ Desenlace: Solución":
    st.title("Optimización mediante Machine Learning (K=5)")
    
    # Definir el color_map basado en la retroalimentación del usuario
    color_map = {
        "Santanderes (Nido de Bucaramanga)": 'blue',
        "Llanos y Piedemonte Orientales": 'purple',
        "Centro y Pacífico Norte (Superficial)": 'yellow',
        "Pacífico Sur (Superficial)": 'red',
        "Sur / Ecuador (Nido Profundo)": 'green'
    }

    # 1. ESTRUCTURA TRIDIMENSIONAL
    st.write("### 🏗️ Estructura Tridimensional")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_3d_1, col_3d_2, col_3d_3 = st.columns([0.1, 0.8, 0.1])
    
    with col_3d_2:
        fig_3d = px.scatter_3d(
            df, x='longitude', y='latitude', z='depth', 
            color='Nombre Región', size='mag_mw',
            color_discrete_map=color_map, opacity=0.9,
            labels={'depth': 'Prof', 'longitude': 'Long', 'latitude': 'Lat'},
            size_max=18,
            hover_name='place'
        )
        fig_3d.update_layout(
            height=750, 
            scene=dict(
                zaxis=dict(autorange="reversed"), 
                aspectratio=dict(x=1, y=1, z=0.6),
                xaxis_title='Longitud',
                yaxis_title='Latitud',
                zaxis_title='Profundidad (km)'
            ),
            margin=dict(l=0, r=0, b=0, t=10),
            legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1}
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    st.write("---")

    # 2. MÉTRICAS DE SELECCIÓN (Codo y Silueta juntos)
    st.write("### 📏 Selección del Modelo")
    col_m1, col_m2 = st.columns(2)
    k_vals = list(range(2, 11))
    # Valores actualizados desde el dataset correcto (2971 registros)
    inertia = [4502.547864853036, 2843.539824649725, 1968.106429994966, 1318.0674512401666, 1146.5492329388334, 1024.1610443212874, 915.2690333207624, 829.4796335198031, 755.3340578672051]
    silhouette = [0.4375503803875322, 0.4900595562723689, 0.5057064223294326, 0.5519890533031021, 0.5350436923491799, 0.4851415174094772, 0.48911571217036667, 0.4969248236712843, 0.4950850829667257]
    
    with col_m1:
        fig_elbow = px.line(x=k_vals, y=inertia, markers=True, title="Método del Codo (Inercia)", labels={'x': 'K', 'y': 'Inercia'})
        fig_elbow.add_vline(x=5, line_dash="dash", line_color="red")
        fig_elbow.update_layout(height=300)
        st.plotly_chart(fig_elbow, use_container_width=True)
    with col_m2:
        fig_sil = px.line(x=k_vals, y=silhouette, markers=True, title="Silhouette Score (Óptimo K=5)", labels={'x': 'K', 'y': 'Score'}, color_discrete_sequence=['#FF8C00'])
        fig_sil.add_vline(x=5, line_dash="dash", line_color="green")
        fig_sil.update_layout(height=300)
        st.plotly_chart(fig_sil, use_container_width=True)

    st.write("---")
    
    # 3. EVOLUCIÓN TEMPORAL
    st.write("### ⏳ Evolución Temporal")
    # Ahora df['year'] se crea en load_all_data
    df_anim = df.dropna(subset=['year']).sort_values('year') 
    fig_anim = px.scatter_mapbox(
        df_anim, lat="latitude", lon="longitude", color="Nombre Región",
        color_discrete_map=color_map, size="mag_mw", size_max=12, 
        animation_frame="year", mapbox_style="carto-positron", zoom=4,
        hover_name="place"
    )
    fig_anim.update_layout(height=550, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_anim, use_container_width=True)

    st.write("---")

    # 4. SNAKE PLOT
    st.write("### 🐍 Snake Plot: Diagnóstico de Salud de la Red")
    st.info("Variables estandarizadas (Z-score). Zonas con **Gap** alto y **NST** bajo son prioridades críticas.")
    
    snake_long = snake.melt(id_vars='cluster', var_name='Variable', value_name='Valor (Z-score)')
    # Usar el mapeo dinámico de cluster_id a nombre de región
    snake_long['Nombre Región'] = snake_long['cluster'].map(cluster_id_to_name_map)

    fig_snake = px.line(
        snake_long, x='Variable', y='Valor (Z-score)', color='Nombre Región',
        color_discrete_map=color_map, markers=True,
        title="Perfiles de Diagnóstico por Región Sísmica"
    )
    fig_snake.update_layout(yaxis_title="Variación vs Media (Z-score)", height=450)
    st.plotly_chart(fig_snake, use_container_width=True)

    st.write("---")

    # 5. PERFILAMIENTO Y COMPARATIVA
    st.write("### 📊 Perfilamiento y Comparativa")
    
    st.write("**Resumen Estadístico por Región**")
    # The profile DataFrame is already loaded and processed in load_all_data()
    # No need to reload it here.
    
    # Usar el mapeo dinámico de cluster_id a nombre de región
    profile['Nombre Región'] = profile.index # Corrected: Directly assign index which already has names

    st.dataframe(profile.style.background_gradient(cmap='Blues'), use_container_width=True)

    params = {
        "mag_mw_mean": "Magnitud Promedio (Mw)", 
        "cluster_count": "Número de Sismos", 
        "depth_mean": "Profundidad Media (km)",
        "gap_mean": "Gap Medio (Grados)",
        "nst_mean": "Estaciones Promedio (NST)"
    }
    selected_param = st.selectbox("Parámetro para comparativa visual:", list(params.keys()), format_func=lambda x: params[x])
    
    fig_bar = px.bar(
        profile, x='Nombre Región', y=selected_param,
        color='Nombre Región', color_discrete_map=color_map,
        title=f"Distribución Regional: {params[selected_param]}",
        labels={selected_param: params[selected_param]}
    )
    fig_bar.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.caption("🔬 Taller 1 - Miguel Camargo. K-Means K=5. Datos: USGS / SGC.")