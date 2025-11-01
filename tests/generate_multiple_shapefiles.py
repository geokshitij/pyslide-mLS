"""
Generate multiple test shapefiles to test the selection feature.
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import box
import os

np.random.seed(42)

print("Generating multiple test shapefiles...")

# Generate two different landslide inventories
for inventory_num in range(1, 3):
    n_landslides = 300 + inventory_num * 100
    true_beta = -2.3 - (inventory_num * 0.1)
    true_cutoff = 100 * inventory_num
    
    # Generate power-law distributed areas
    u = np.random.uniform(0, 1, n_landslides)
    alpha = abs(true_beta) - 1
    areas = true_cutoff * (1 - u) ** (-1/alpha)
    
    # Create polygons
    geometries = []
    for i, area in enumerate(areas):
        side = np.sqrt(area)
        x = np.random.uniform(0, 100000)
        y = np.random.uniform(0, 100000)
        geom = box(x, y, x + side, y + side)
        geometries.append(geom)
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        {
            'id': range(n_landslides),
            'area_m2': areas,
            'inventory': f'Inventory_{inventory_num}'
        },
        geometry=geometries,
        crs='EPSG:32633'
    )
    
    # Save to shapefile
    output_file = f'landslides_inventory{inventory_num}.shp'
    gdf.to_file(output_file)
    
    print(f"\n✅ Created {output_file}")
    print(f"   Landslides: {n_landslides}")
    print(f"   Beta: {true_beta}")
    print(f"   Cutoff: {true_cutoff} m²")

print("\n📦 Creating ZIP with multiple shapefiles...")
import zipfile

with zipfile.ZipFile('multiple_landslides.zip', 'w') as zipf:
    for inventory_num in range(1, 3):
        base_name = f'landslides_inventory{inventory_num}'
        for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
            filename = base_name + ext
            if os.path.exists(filename):
                zipf.write(filename)

print("✅ Created multiple_landslides.zip")
print("\nThis ZIP contains 2 shapefiles:")
print("  - landslides_inventory1.shp (400 features)")
print("  - landslides_inventory2.shp (500 features)")
print("\nUpload this to test the shapefile selection feature!")
