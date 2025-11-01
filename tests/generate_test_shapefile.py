"""
Generate a test shapefile with synthetic landslide polygons for testing the mLS calculator.
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import box
import os

# Set random seed for reproducibility
np.random.seed(42)

print("Generating test landslide shapefile...")

# Generate power-law distributed landslide sizes
n_landslides = 500
true_beta = -2.3
true_cutoff = 100

# Generate power-law distributed areas
u = np.random.uniform(0, 1, n_landslides)
alpha = abs(true_beta) - 1
areas = true_cutoff * (1 - u) ** (-1/alpha)

# Create polygons with these areas
geometries = []
for i, area in enumerate(areas):
    # Calculate square dimensions
    side = np.sqrt(area)
    
    # Random location in a 100km x 100km area
    x = np.random.uniform(0, 100000)
    y = np.random.uniform(0, 100000)
    
    # Create square polygon
    geom = box(x, y, x + side, y + side)
    geometries.append(geom)

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    {
        'id': range(n_landslides),
        'area_m2': areas
    },
    geometry=geometries,
    crs='EPSG:32633'  # UTM Zone 33N
)

# Save to shapefile
output_file = 'test_landslides.shp'
gdf.to_file(output_file)

print(f"✅ Created {output_file}")
print(f"   Number of landslides: {n_landslides}")
print(f"   Total area: {areas.sum():.2e} m²")
print(f"   Min area: {areas.min():.2f} m²")
print(f"   Max area: {areas.max():.2f} m²")
print(f"   Mean area: {areas.mean():.2f} m²")
print(f"   Median area: {np.median(areas):.2f} m²")
print(f"\nExpected mLS parameters:")
print(f"   True beta: {true_beta}")
print(f"   True cutoff: {true_cutoff} m²")
print(f"\nNow zip the shapefile components for upload:")
print(f"   zip test_landslides.zip test_landslides.*")
