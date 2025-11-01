# 🚀 Quick Reference Guide

## Starting the Application

```bash
# Navigate to project directory
cd /Users/kdahal3/Desktop/pyslide-mLS

# Option 1: Use the convenience script
./run.sh

# Option 2: Manual start
source venv/bin/activate
python app.py
```

Then open: **http://localhost:5000**

---

## First Time Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test installation
python test_installation.py

# 5. Run the app
python app.py
```

---

## File Requirements

### Shapefile ZIP must contain:
- ✅ `.shp` - geometry
- ✅ `.shx` - shape index  
- ✅ `.dbf` - attributes
- ✅ `.prj` - projection
- ⚠️  Should contain **polygon** features

---

## Common Commands

### Stop the server
```bash
Ctrl + C
```

### Deactivate virtual environment
```bash
deactivate
```

### Update dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Check if port 5000 is available
```bash
lsof -ti:5000
```

### Kill process on port 5000
```bash
lsof -ti:5000 | xargs kill -9
```

---

## Typical Workflow

1. **Start app** → `./run.sh`
2. **Open browser** → http://localhost:5000
3. **Upload shapefile** → ZIP with all components
4. **Enter parameters** (optional) → Leave blank for auto-estimate
5. **Calculate** → Click "Calculate mLS"
6. **View results** → mLS value, plot, and statistics
7. **Download results** (optional) → Save plot image

---

## Power-Law Parameters

### Auto-estimation (Recommended for first-time users)
- Leave fields **blank**
- System estimates cutoff and beta automatically

### Manual entry (For experienced users)
- **Cutoff**: Minimum area following power-law (m²)
- **Beta**: Power-law exponent (-1.4 to -3.4 typical)
- **Errors**: Optional uncertainty values

---

## Expected Results

### For sample data:
- **Beta**: ~-2.46
- **mLS**: ~3.63 ± 0.08

### Typical ranges:
- **Small events**: mLS < 3
- **Moderate events**: mLS 3-4
- **Large events**: mLS 4-5
- **Very large events**: mLS > 5

---

## Troubleshooting Quick Fixes

### Import errors
```bash
pip install -r requirements.txt
```

### GDAL issues (macOS)
```bash
brew install gdal
```

### GDAL issues (Linux)
```bash
sudo apt-get install gdal-bin libgdal-dev
```

### Port in use
```bash
lsof -ti:5000 | xargs kill -9
```

### Permission denied for run.sh
```bash
chmod +x run.sh
```

---

## File Locations

- **Application**: `app.py`
- **Calculator**: `mls_calculator.py`
- **Templates**: `templates/`
- **Requirements**: `requirements.txt`
- **Setup guide**: `PYTHON_SETUP.md`
- **Full README**: `README_PYTHON.md`

---

## URLs When Running

- **Home/Upload**: http://localhost:5000
- **About**: http://localhost:5000/about

---

## Tips

💡 **First time?** Use the About page for methodology details

💡 **Large files?** Increase timeout in `app.py`

💡 **Production use?** Change secret key and use proper WSGI server

💡 **Testing?** Run `python test_installation.py`

💡 **Need help?** Check `PYTHON_SETUP.md` for detailed guide

---

## Citation

```
Tanyas, H., K.E. Allstadt, and C.J. van Westen, 2018, 
An updated method for estimating landslide-event magnitude, 
Earth Surface Processes and Landforms. DOI: 10.1002/esp.4359
```

---

**Need more help?** See [PYTHON_SETUP.md](PYTHON_SETUP.md) for comprehensive documentation.
