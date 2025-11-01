# 🔧 Troubleshooting Guide

## Common Issues and Solutions

---

### ❌ Issue: `ModuleNotFoundError: No module named 'flask'`

**Cause:** Dependencies not installed or virtual environment not activated.

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### ❌ Issue: `ModuleNotFoundError: No module named 'geopandas'`

**Cause:** GeoPandas installation failed (usually GDAL-related).

**Solution:**

**On macOS:**
```bash
# Install GDAL first
brew install gdal

# Then install GeoPandas
pip install geopandas
```

**On Ubuntu/Debian:**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev python3-gdal

# Install GeoPandas
pip install geopandas
```

**On Windows:**
```bash
# Use conda instead of pip
conda install -c conda-forge geopandas
```

---

### ❌ Issue: `Address already in use` / `Port 5000 is in use`

**Cause:** Another process is using port 5000.

**Solution 1 - Kill the process:**
```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution 2 - Use a different port:**
Edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Changed from 5000
```

---

### ❌ Issue: `Permission denied: './run.sh'`

**Cause:** Script is not executable.

**Solution:**
```bash
chmod +x run.sh
```

---

### ❌ Issue: Shapefile upload fails with "No .shp file found"

**Cause:** ZIP file doesn't contain required shapefile components.

**Solution:**
Ensure your ZIP contains ALL of these files:
- ✅ `filename.shp` (geometry)
- ✅ `filename.shx` (shape index)
- ✅ `filename.dbf` (attributes)
- ✅ `filename.prj` (projection)

Create the ZIP properly:
```bash
# On macOS/Linux
zip landslides.zip landslides.shp landslides.shx landslides.dbf landslides.prj

# On Windows (PowerShell)
Compress-Archive -Path *.shp,*.shx,*.dbf,*.prj -DestinationPath landslides.zip
```

---

### ❌ Issue: "Shapefile has no coordinate reference system (CRS) defined"

**Cause:** Missing or invalid `.prj` file.

**Solution:**
Add a proper `.prj` file to your shapefile. If you know the CRS:

**For WGS84 (EPSG:4326):**
Create `filename.prj` with:
```
GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]
```

**For UTM Zone 33N (EPSG:32633):**
Create `filename.prj` with:
```
PROJCS["WGS_1984_UTM_Zone_33N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",15],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["Meter",1]]
```

Or use a GIS tool (QGIS, ArcGIS) to set the CRS.

---

### ❌ Issue: "No valid polygons found in shapefile"

**Cause:** 
- Shapefile contains points/lines instead of polygons
- All polygons are too small (< 1 m²)
- Geometries are invalid

**Solution:**

**Check geometry type:**
```python
import geopandas as gpd
gdf = gpd.read_file('your_file.shp')
print(gdf.geometry.type.unique())  # Should show 'Polygon' or 'MultiPolygon'
```

**Fix invalid geometries:**
```python
gdf['geometry'] = gdf['geometry'].buffer(0)
gdf.to_file('fixed_file.shp')
```

---

### ❌ Issue: mLS value seems incorrect or is NaN

**Cause:** 
- Insufficient data (too few landslides)
- Invalid parameter values
- Data doesn't follow power-law distribution

**Solution:**

1. **Check data size:** Need at least 50-100 landslides
2. **Check area range:** Should span several orders of magnitude
3. **Check parameters:** 
   - Beta should be negative (-1.4 to -3.4 typical)
   - Cutoff should be within your data range
4. **Try automatic estimation:** Leave parameters blank

---

### ❌ Issue: Plot doesn't display or shows as broken image

**Cause:** Matplotlib backend issues or encoding problem.

**Solution:**

Check that `mls_calculator.py` has:
```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
```

If still broken, try:
```bash
pip install --upgrade matplotlib pillow
```

---

### ❌ Issue: "File too large" error

**Cause:** File exceeds maximum upload size (default 50MB).

**Solution:**

Edit `app.py` and increase the limit:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

Or compress your shapefile better (remove unnecessary attributes).

---

### ❌ Issue: Virtual environment not activating

**Cause:** Virtual environment not created properly or shell issues.

**Solution:**

**On macOS/Linux:**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Verify it's activated (should show (venv) in prompt)
which python  # Should point to venv/bin/python
```

**On Windows:**
```cmd
# PowerShell
venv\Scripts\Activate.ps1

# CMD
venv\Scripts\activate.bat
```

---

### ❌ Issue: Application runs but webpage doesn't load

**Cause:** Firewall, wrong URL, or server not binding correctly.

**Solution:**

1. **Check the URL:** Should be `http://localhost:5000` (not https)
2. **Check firewall:** Allow Python through firewall
3. **Try 127.0.0.1:**  `http://127.0.0.1:5000`
4. **Check Flask output:** Should show "Running on http://0.0.0.0:5000"

---

### ❌ Issue: "Internal Server Error" (500)

**Cause:** Python exception in the application.

**Solution:**

1. **Check Flask console:** Look for error traceback
2. **Enable debug mode:** Should be on by default in `app.py`
3. **Common causes:**
   - Missing templates
   - Import errors
   - File permission issues

**Enable verbose error reporting:**
```python
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
```

---

### ❌ Issue: "Uncertainty: Not calculated" in results

**Cause:** Beta error and cutoff error not provided.

**Solution:**

This is normal if you didn't enter error values. To get uncertainty:

1. **Let system estimate:** Automatic estimation includes errors
2. **Or provide manually:** Enter beta_error and cutoff_error in form
3. **Or calculate with plfit.m:** Use MATLAB plfit.m and plvar.m

---

### ❌ Issue: Results differ from MATLAB version

**Cause:** 
- Different input parameters
- Different random seed for Monte Carlo
- Numerical precision differences

**Solution:**

1. **Check parameters match:** Ensure cutoff and beta are identical
2. **Expected difference:** Small differences (< 0.1) in mLS are normal
3. **Large differences:** Check input areas are the same

---

### ❌ Issue: Installation test fails

**Cause:** Dependencies not properly installed.

**Solution:**

```bash
# Run test with verbose output
python test_installation.py

# Reinstall problematic packages
pip uninstall <package-name>
pip install <package-name>

# Or reinstall everything
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## Platform-Specific Issues

### macOS

**Issue: SSL Certificate Error**
```bash
# Install certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

**Issue: Command Line Tools**
```bash
xcode-select --install
```

### Linux

**Issue: Python 3.8+ not available**
```bash
# Ubuntu 18.04/20.04
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv
```

### Windows

**Issue: Long path issues**
- Enable long paths in Windows
- Or move project to shorter path (e.g., `C:\mls\`)

**Issue: Visual C++ required**
- Install Microsoft Visual C++ Build Tools
- Or use Anaconda distribution

---

## Performance Issues

### Large shapefiles (>10,000 features) are slow

**Solutions:**
1. Simplify geometries before upload
2. Increase Flask timeout
3. Use a production server (Gunicorn)
4. Process in batches

### Memory errors

**Solutions:**
1. Close other applications
2. Increase available RAM
3. Process smaller subsets
4. Use a more powerful machine

---

## Getting Help

If your issue isn't listed here:

1. **Check detailed docs:** See [PYTHON_SETUP.md](PYTHON_SETUP.md)
2. **Check Flask logs:** Look at terminal output
3. **Enable debug mode:** See detailed error pages
4. **Test with sample data:** Verify basic functionality
5. **Check Python version:** Ensure 3.8+
6. **Verify all dependencies:** Run `test_installation.py`

---

## Still Having Issues?

Create a minimal test case:

```python
# test_minimal.py
from mls_calculator import calculate_mls
import numpy as np

# Generate test data
areas = np.random.lognormal(5, 2, 100) * 100

# Try calculation
try:
    mls, error, plot = calculate_mls(areas, 100, -2.3)
    print(f"Success! mLS = {mls}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

Run it:
```bash
python test_minimal.py
```

This isolates whether the issue is with:
- Core calculation (mls_calculator.py)
- Flask/web (app.py)
- Shapefile processing (geopandas)

---

## Quick Diagnostic Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip list`)
- [ ] GDAL installed (if on macOS/Linux)
- [ ] Port 5000 available
- [ ] `test_installation.py` passes
- [ ] Shapefile has all required files (.shp, .shx, .dbf, .prj)
- [ ] Shapefile contains polygons (not points/lines)
- [ ] CRS is defined in .prj file
- [ ] File size under 50MB (or limit increased)

---

**Last Resort:** Delete everything and start fresh:
```bash
cd /Users/kdahal3/Desktop/pyslide-mLS
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python test_installation.py
./run.sh
```
