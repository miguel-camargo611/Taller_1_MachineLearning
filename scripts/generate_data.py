import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, silhouette_samples
import warnings
warnings.filterwarnings('ignore')

# 1. Cargar datos desde la URL oficial
url = (
 "https://zcecnewftnpelovbnutv.supabase.co"
 "/storage/v1/object/public/project-files"
 "/academy/ml1/earthquakes_colombia.csv"
)
print(f"Descargando datos desde: {url}")
df = pd.read_csv(url)
df['time'] = pd.to_datetime(df['time'], format='ISO8601', utc=True)

# 2. Normalizar magnitudes a Mw
print("Normalizando unidades de magnitud a Mw...")
def normalize_to_mw(row):
    mag, mtype = row['mag'], str(row['magType']).lower()
    if mtype in ['mb', 'ml']: return 0.85 * mag + 1.03
    if mtype == 'ms': return 0.67 * mag + 2.13
    return mag

df['mag_mw'] = df.apply(normalize_to_mw, axis=1)
df['magType'] = 'Mw'

total_records = len(df)
print(f"Total registros obtenidos: {total_records}")

# 3. Preparación de datos para Clustering
# Limpiar nulos para el clustering
features = ['latitude', 'longitude', 'depth']
X = df[features].fillna(df[features].median())

# Escalar
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Corriendo KMeans (K=5)
print("Corriendo KMeans con K=5 (Óptimo)...")
K_optimo = 5
km_scaled = KMeans(n_clusters=K_optimo, random_state=42).fit(X_scaled)
df["cluster"] = km_scaled.labels_

# Mapeo de nombres dinámicos basado en geografía y profundidad
means = df.groupby("cluster")[["latitude", "depth"]].mean()
cluster_names = {}

for idx, row in means.iterrows():
    lat, depth = row["latitude"], row["depth"]
    if depth > 100:
        if lat > 0: cluster_names[idx] = "Santanderes (Nido de Bucaramanga)"
        else: cluster_names[idx] = "Sur / Ecuador (Nido Profundo)"
    else:
        if lat < 0: cluster_names[idx] = "Pacífico Sur (Superficial)"
        elif lat > 7.5: cluster_names[idx] = "Llanos y Piedemonte Orientales"
        else: cluster_names[idx] = "Centro y Pacífico Norte (Superficial)"

df["cluster_name"] = df["cluster"].map(cluster_names)

# 5. Exportar base principal (clustered_data.csv)
print("Exportando data/clustered_data.csv...")
df.to_csv('data/clustered_data.csv', index=False)

# 6. Generar cluster profile
print("Generando data/cluster_profile.csv...")
stats = df.groupby('cluster_name').agg({
    'mag_mw': ['mean', 'median', 'std', 'min', 'max'],
    'depth': ['mean', 'median', 'std'],
    'latitude': ['mean', 'std'],
    'longitude': ['mean', 'std'],
    'nst': ['mean', 'median'],
    'gap': ['mean', 'median'],
    'cluster': ['count']
}).round(2)

stats.to_csv('data/cluster_profile.csv')

# 7. Generar Snake Plot Data (Z-scores)
print("Generando data/snake_data.csv...")
snake_vars = ['gap', 'nst', 'mag_mw', 'depth']
cluster_means = df.groupby('cluster')[snake_vars].mean()

scaler_snake = StandardScaler()
snake_scaled = scaler_snake.fit_transform(cluster_means)
snake_df = pd.DataFrame(snake_scaled, columns=snake_vars)
snake_df['cluster'] = cluster_means.index

cols = ['cluster'] + snake_vars
snake_df = snake_df[cols]
snake_df.to_csv('data/snake_data.csv', index=False)

# 8. Cálculos de verificación para el Dashboard
print("\n--- Verificación de Métricas para el Dashboard ---")
inertia = []
silhouette = []
K_range = range(2, 11)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42).fit(X_scaled)
    inertia.append(km.inertia_)
    silhouette.append(silhouette_score(X_scaled, km.labels_))

print(f"Inertia_values = {inertia}")
print(f"Silhouette_values = {silhouette}")

print("\n--- ¡Proceso finalizado con éxito! ---")

