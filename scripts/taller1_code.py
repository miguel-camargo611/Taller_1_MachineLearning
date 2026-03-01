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

df = pd.read_csv('data/earthquakes.csv') # Make sure this path is correct
df['time'] = pd.to_datetime(df['time'], format='ISO8601', utc=True)

def normalize_to_mw(row):
    mag, mtype = row['mag'], str(row['magType']).lower()
    if mtype in ['mb', 'ml']: return 0.85 * mag + 1.03
    if mtype == 'ms': return 0.67 * mag + 2.13
    return mag

df['mag_mw'] = df.apply(normalize_to_mw, axis=1)

total_records = len(df)
colombia_records = len(df[(df.latitude > -4.5) & (df.latitude < 13.5) & (df.longitude > -82) & (df.longitude < -66.5)])

print(f"¿Cuántos registros tienes en total? {total_records}")
print(f"¿Cuántos corresponden a Colombia específicamente? {colombia_records}")
# --- CELL ---
nulls = df.isnull().mean() * 100
print("Porcentaje de nulos por variable:")
print(nulls[nulls > 0])
# --- CELL ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(df['mag_mw'], kde=True, ax=ax1, color='orange')
ax1.set_title('Distribución de Magnitudes (Mw)')
ax1.set_xlabel('Magnitud Mw')

sns.histplot(df['depth'], kde=True, ax=ax2, color='blue')
ax2.set_title('Distribución de Profundidades (km)')
ax2.set_xlabel('Profundidad (km)')

plt.show()
# --- CELL ---
plt.figure(figsize=(8, 5))
sns.heatmap(df[['latitude', 'longitude', 'depth', 'mag_mw', 'nst', 'gap']].corr(), annot=True, cmap='coolwarm')
plt.title('Matriz de Correlación')
plt.show()
# --- CELL ---
features = ['latitude', 'longitude', 'depth']
X = df[features].fillna(df[features].median())
# --- CELL ---
# Sin Escalar
km_raw = KMeans(n_clusters=5, random_state=42).fit(X)
score_raw = silhouette_score(X, km_raw.labels_)

# Con Escalar
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
km_scaled = KMeans(n_clusters=5, random_state=42).fit(X_scaled)
score_scaled = silhouette_score(X_scaled, km_scaled.labels_)

print(f"Silhouette Score Sin Escalar: {score_raw:.4f}")
print(f"Silhouette Score Con Escalar: {score_scaled:.4f}")
# --- CELL ---
inertia = []
silhouette = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42).fit(X_scaled)
    inertia.append(km.inertia_)
    silhouette.append(silhouette_score(X_scaled, km.labels_))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
ax1.plot(K_range, inertia, 'bo-')
ax1.set_title('Método del Codo (Inercia)')
ax1.set_xlabel('Número de Clústeres (K)')
ax1.set_ylabel('Inercia')

ax2.plot(K_range, silhouette, 'ro-')
ax2.set_title('Silhouette Score por K')
ax2.set_xlabel('K')
ax2.set_ylabel('Score')
plt.show()
# --- CELL ---
df["cluster"] = km_scaled.labels_

# Mapeo dinámico para asegurar que los nombres coincidan con la geografía
# sin importar el ID (0-4) que asigne el algoritmo localmente.
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

# --- CELL ---
# 1. Calculate unscaled cluster centroids
unscaled_centroids = scaler.inverse_transform(km_scaled.cluster_centers_)
centroids_df = pd.DataFrame(unscaled_centroids, columns=features)

# 2. Add cluster and cluster_name to centroids_df
centroids_df['cluster'] = range(len(centroids_df))
centroids_df['cluster_name'] = centroids_df['cluster'].map(cluster_names) # Use the same cluster_names mapping

# Create a custom palette based on user feedback
custom_palette = {
    'Llanos y Piedemonte Orientales': 'purple',
    'Santanderes (Nido de Bucaramanga)': 'blue',
    'Centro y Pacífico Norte (Superficial)': 'orange',
    'Pacífico Sur (Superficial)': 'red',
    'Sur / Ecuador (Nido Profundo)': 'green'
}

# 3. Modify the scatter plot
plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='longitude', y='latitude', hue='cluster_name', palette=custom_palette, s=25, alpha=0.7)
sns.scatterplot(data=centroids_df, x='longitude', y='latitude', color='black',
                marker='X', s=200, edgecolor='white', linewidth=1, legend=False) # Plot centroids with black color
plt.title('Zonificación Sísmica Final por Clustering (K=5)')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
plt.gca().set_aspect('equal', adjustable='box') # Proporción real
plt.show()