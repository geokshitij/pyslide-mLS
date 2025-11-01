# Python Flask Web Application for mLS Calculator

This directory contains a **Python/Flask web application** for calculating landslide-event magnitude (mLS) from shapefile data. This is a new implementation that provides a web-based interface for the mLS calculation method.

## 🎯 What This Does

- **Converts the MATLAB `mLS.m` code to Python** (the original MATLAB code remains unchanged)
- Provides a **web-based user interface** for uploading shapefiles
- **Automatically calculates landslide areas** from shapefile polygons
- **Estimates power-law parameters** (cutoff and beta) or accepts user-provided values
- **Calculates mLS values** with uncertainty estimation
- **Generates frequency-area distribution plots**

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

### Step 1: Create a Virtual Environment (Recommended)

```bash
# Navigate to the project directory
cd /Users/kdahal3/Desktop/pyslide-mLS

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** Installing `geopandas` and its dependencies may take a few minutes. If you encounter issues, you may need to install GDAL separately:

On macOS:
```bash
brew install gdal
```

On Ubuntu/Debian:
```bash
sudo apt-get install gdal-bin libgdal-dev
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

Open your web browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
pyslide-mLS/
├── app.py                      # Flask web application
├── mls_calculator.py           # Python conversion of mLS.m
├── powerlaw_estimator.py       # Automatic power-law parameter estimation
├── requirements.txt            # Python dependencies
├── templates/                  # HTML templates
│   ├── base.html              # Base template with layout
│   ├── index.html             # Upload form page
│   ├── results.html           # Results display page
│   └── about.html             # About/methodology page
├── mLS.m                       # Original MATLAB code (unchanged)
├── sample_data.mat             # Sample data
└── README.md                   # Original README
```

## 💻 Usage

### Basic Usage

1. **Start the application** (see Installation Step 3)
2. **Open your browser** to `http://localhost:5000`
3. **Upload a shapefile**:
   - Click the upload box or drag-and-drop a ZIP file
   - ZIP must contain: `.shp`, `.shx`, `.dbf`, and `.prj` files
   - Shapefile should contain polygon features (landslides)
4. **Optional: Enter power-law parameters**:
   - Leave blank for automatic estimation
   - Or enter pre-calculated cutoff, beta, and error values
5. **Click "Calculate mLS"**
6. **View results**:
   - mLS value with uncertainty
   - Frequency-area distribution plot
   - Detailed statistics

### Shapefile Requirements

- **Format:** ZIP file containing shapefile components
- **Geometry Type:** Polygons (representing landslide boundaries)
- **CRS:** Must have a defined coordinate reference system
- **Area Calculation:** 
  - If CRS is geographic (lat/lon), it will be automatically reprojected to UTM
  - Areas are calculated in square meters (m²)

### Power-Law Parameters

You can either:

1. **Let the system estimate** (leave fields empty):
   - Automatic estimation using methods similar to Clauset et al. (2009)
   - Good for quick analysis or when you don't have pre-calculated values

2. **Provide your own values**:
   - Use tools like `plfit.m` from Clauset et al. (2009)
   - Enter cutoff (xmin), beta (β), and optionally their errors
   - More accurate if you have domain knowledge

## 📊 Example Workflow

### Using Sample Data

To test the application with the provided sample data:

1. You'll need to convert `sample_data.mat` to a shapefile first, OR
2. Use your own landslide inventory shapefile from `/Users/kdahal3/Desktop/shapefile`

### Creating Synthetic Test Data

```python
# Run this to create a test shapefile:
python -c "
import geopandas as gpd
import numpy as np
from shapely.geometry import box
import pandas as pd

# Create synthetic landslide polygons
np.random.seed(42)
n_landslides = 500

# Generate random locations and sizes
geometries = []
for i in range(n_landslides):
    # Random position
    x = np.random.uniform(0, 10000)
    y = np.random.uniform(0, 10000)
    # Power-law distributed size
    size = np.random.pareto(2.3) * 100 + 50
    geometries.append(box(x, y, x+size, y+size))

# Create GeoDataFrame
gdf = gpd.GeoDataFrame({'id': range(n_landslides)}, geometry=geometries, crs='EPSG:32633')
gdf.to_file('test_landslides.shp')
print('Test shapefile created: test_landslides.shp')
"
```

Then zip the shapefile components:
```bash
zip test_landslides.zip test_landslides.*
```

## 🔧 Configuration

### Port Configuration

To run on a different port, edit `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change 5000 to your desired port
```

### File Size Limits

The default maximum upload size is 50MB. To change this, edit `app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### Secret Key

For production use, change the secret key in `app.py`:

```python
app.config['SECRET_KEY'] = 'your-secure-random-key-here'
```

## 🐛 Troubleshooting

### GDAL Installation Issues

If you have trouble installing geopandas:

**macOS:**
```bash
brew install gdal
export GDAL_CONFIG=/opt/homebrew/bin/gdal-config
pip install gdal==$(gdal-config --version)
pip install geopandas
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev python3-gdal
pip install geopandas
```

### Port Already in Use

If port 5000 is already in use:
```bash
# Kill the process using port 5000
lsof -ti:5000 | xargs kill -9

# Or run on a different port (edit app.py)
```

### Shapefile CRS Issues

If you get CRS-related errors:
- Ensure your shapefile has a `.prj` file
- Check that the CRS is defined and valid
- Try reprojecting your shapefile before upload

## 📚 References

**Primary Reference:**
Tanyas, H., Allstadt, K.E., and van Westen, C.J., 2018. An updated method for estimating landslide-event magnitude. Earth Surface Processes and Landforms, 43(9), pp.1836-1847. DOI: [10.1002/esp.4359](https://doi.org/10.1002/esp.4359)

**Power-Law Estimation:**
Clauset, A., Shalizi, C.R. and Newman, M.E., 2009. Power-law distributions in empirical data. SIAM review, 51(4), pp.661-703. DOI: [10.1137/070710111](https://doi.org/10.1137/070710111)

## 📝 Citation

If you use this tool in your research, please cite the original paper:

```
Tanyas, H., K.E. Allstadt, and C.J. van Westen, 2018, 
An updated method for estimating landslide-event magnitude, 
Earth Surface Processes and Landforms. DOI: 10.1002/esp.4359
```

## ⚖️ License

See LICENSE.md in the repository root.

## 🤝 Contributing

This is a research tool. The original MATLAB code (`mLS.m`) has not been modified. The Python implementation provides equivalent functionality with a web-based interface.

## 📧 Support

For questions about the methodology, refer to the original paper by Tanyas et al. (2018).

For technical issues with this Python implementation, please check:
1. That all dependencies are correctly installed
2. That your Python version is 3.8 or higher
3. That your shapefile is properly formatted with all required components
