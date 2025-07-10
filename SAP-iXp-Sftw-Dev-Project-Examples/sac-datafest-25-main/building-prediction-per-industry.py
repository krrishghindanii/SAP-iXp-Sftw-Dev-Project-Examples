import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import osmnx as ox
import numpy as np
from shapely.geometry import Point
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D

# --- Load Manhattan ---
place = "Manhattan, New York, USA"
manhattan_poly = ox.geocode_to_gdf(place).geometry.iloc[0]

# --- Download buildings and assign industry based on size ---
buildings = ox.features_from_place(place, {"building": True})
buildings = buildings.to_crs("EPSG:3857")
buildings['area_m2'] = buildings.geometry.area
buildings = buildings.to_crs("EPSG:4326")
buildings = buildings[buildings['area_m2'] > 1000]

def classify_industry(area):
    if area > 20000:
        return "Tech"
    elif area > 10000:
        return "Finance"
    else:
        return "Legal"

buildings['Industry'] = buildings['area_m2'].apply(classify_industry)

# --- Sample equal number of buildings from each category ---
np.random.seed(2024)
sample_size = 100
balanced_samples = pd.concat([
    buildings[buildings['Industry'] == ind].sample(n=min(sample_size, len(buildings[buildings['Industry'] == ind])), random_state=42)
    for ind in ['Tech', 'Finance', 'Legal']
])

# --- Create synthetic lease GeoDataFrame ---
centroids = balanced_samples.geometry.centroid
gdf = gpd.GeoDataFrame({
    'Longitude': centroids.x,
    'Latitude': centroids.y,
    'Industry': balanced_samples['Industry'].values,
    'Area_m2': balanced_samples['area_m2'].values
}, geometry=centroids, crs="EPSG:4326")

# --- Group by location to simulate clusters ---
gdf['grid_id'] = (gdf['Latitude'] * 100).astype(int).astype(str) + "-" + (gdf['Longitude'] * 100).astype(int).astype(str)
grouped = gdf.groupby(['grid_id', 'Industry']).agg({
    'Latitude': 'mean',
    'Longitude': 'mean',
    'Area_m2': 'mean',
    'Industry': 'count'
}).rename(columns={'Industry': 'Count'}).reset_index()

# Normalize size for plotting
norm = Normalize(vmin=grouped['Count'].min(), vmax=grouped['Count'].max())
grouped['Size'] = 50 + 250 * norm(grouped['Count'])

# --- Load map layers ---
graph = ox.graph_from_place(place, network_type="drive")
nodes, edges = ox.graph_to_gdfs(graph)
parks = ox.features_from_place(place, {"leisure": "park"})

# --- Plotting ---
fig, ax = plt.subplots(figsize=(14, 14))
ax.set_facecolor("#e6f2ff")
edges.plot(ax=ax, linewidth=0.4, edgecolor="dimgray", zorder=1)

if not parks.empty:
    parks.plot(ax=ax, facecolor="lightgreen", edgecolor="green", alpha=0.6, zorder=2)

if not buildings.empty:
    buildings.plot(
        ax=ax,
        facecolor="lightgray",
        edgecolor="saddlebrown",
        alpha=0.5,
        linewidth=0.2,
        path_effects=[pe.withSimplePatchShadow(offset=(1, -1), shadow_rgbFace='gray')],
        zorder=3
    )

# --- Plot clusters ---
industry_colors = {'Tech': '#e41a1c', 'Finance': '#4daf4a', 'Legal': '#377eb8'}
for industry, color in industry_colors.items():
    ind_data = grouped[grouped['Industry'] == industry]
    ax.scatter(
        ind_data['Longitude'], ind_data['Latitude'],
        s=ind_data['Size'], color=color,
        label=industry, alpha=0.8, edgecolor='black', linewidth=0.4, zorder=4
    )

# --- Fixed-size legend markers ---
legend_handles = [
    Line2D([0], [0], marker='o', color='w', label='Tech (sqft > 20,000)',
           markerfacecolor=industry_colors['Tech'], markersize=10, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label='Finance (sqft > 10,000)',
           markerfacecolor=industry_colors['Finance'], markersize=10, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label='Legal',
           markerfacecolor=industry_colors['Legal'], markersize=10, markeredgecolor='black')
]

ax.legend(handles=legend_handles, title="Inferred Industry", loc="upper left")
ax.set_title("Manhattan 2024 – Balanced Lease Clusters by Industry", fontsize=26, weight='bold')
ax.axis("off")
plt.tight_layout()
plt.savefig("manhattan_balanced_clusters.png", dpi=300, bbox_inches='tight')
plt.show()
