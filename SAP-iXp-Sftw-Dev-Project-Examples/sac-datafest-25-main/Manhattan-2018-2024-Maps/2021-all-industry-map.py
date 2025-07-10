import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from shapely.geometry import Point
import osmnx as ox
import numpy as np
from matplotlib.colors import Normalize

# Get Manhattan polygon
place = "Manhattan, New York, USA"
manhattan_poly = ox.geocode_to_gdf(place).geometry.iloc[0]

# Generate random points inside Manhattan
def generate_points_within(polygon, n):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < n:
        p = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
        if polygon.contains(p):
            points.append(p)
    return points

# Set seed and generate new data for 2021
np.random.seed(2021)
n_points = 300
points = generate_points_within(manhattan_poly, n_points)

# Assign industries and quarters
industries = np.random.choice(['Tech', 'Legal', 'Finance'], size=n_points)
quarters = np.random.choice(['Q1', 'Q2', 'Q3', 'Q4'], size=n_points)

# Create DataFrame
df = pd.DataFrame({
    'Latitude': [p.y for p in points],
    'Longitude': [p.x for p in points],
    'Industry': industries,
    'Quarter': quarters
})

# GeoDataFrame
geometry = points
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Create grid IDs (for grouping only)
gdf['grid_id'] = (gdf['Latitude']*100).astype(int).astype(str) + "-" + (gdf['Longitude']*100).astype(int).astype(str)

# Get map layers
graph = ox.graph_from_place(place, network_type="drive")
nodes, edges = ox.graph_to_gdfs(graph)
buildings = ox.geometries_from_place(place, {"building": True})
parks = ox.geometries_from_place(place, {"leisure": "park"})

# Plot setup
fig, ax = plt.subplots(figsize=(14, 14))
ax.set_facecolor("#e6f2ff")
ax.set_title("Manhattan Industry Lease Clusters – 2021", fontsize=20, weight='bold')

# Base map
edges.plot(ax=ax, linewidth=0.4, edgecolor="dimgray", zorder=1)
if parks is not None and not parks.empty:
    parks.plot(ax=ax, facecolor="lightgreen", edgecolor="green", alpha=0.6, zorder=2)
if buildings is not None and not buildings.empty:
    buildings.plot(
        ax=ax,
        facecolor="peru",
        edgecolor="saddlebrown",
        alpha=0.85,
        linewidth=0.2,
        path_effects=[pe.withSimplePatchShadow(offset=(2, -2), shadow_rgbFace='gray')],
        zorder=3
    )

# Group data for clustering
grouped = gdf.groupby(['grid_id', 'Industry']).agg({
    'Latitude': 'mean',
    'Longitude': 'mean',
    'Industry': 'count'
}).rename(columns={'Industry': 'Count'}).reset_index()

# Normalize sizes
norm = Normalize(vmin=grouped['Count'].min(), vmax=grouped['Count'].max())
grouped['Size'] = 50 + 250 * norm(grouped['Count'])

# Industry colors
industry_colors = {'Tech': 'red', 'Legal': 'blue', 'Finance': 'green'}

# Plot industry dots
for ind in industry_colors:
    ind_data = grouped[grouped['Industry'] == ind]
    ax.scatter(ind_data['Longitude'], ind_data['Latitude'],
               s=ind_data['Size'], color=industry_colors[ind], label=ind, alpha=0.8, zorder=4)

# Hide axis
ax.axis("off")

# Legend
plt.legend()
plt.tight_layout()
plt.savefig("manhattan_industry_clusters_2021.png", dpi=300, bbox_inches='tight')
plt.close()
