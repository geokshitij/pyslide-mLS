# 🏔️ mLS Calculator - Python Flask Web Application

A web-based tool for calculating **landslide-event magnitude (mLS)** from shapefile data.

This is a **Python implementation** of the MATLAB code from Tanyas et al. (2018), providing an easy-to-use web interface for landslide magnitude estimation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-See%20LICENSE.md-orange.svg)

---

## 🎯 Features

- **✨ Web-based interface** - No MATLAB required!
- **📁 Shapefile upload** - Drag-and-drop ZIP files containing shapefiles
- **🔄 Automatic area calculation** - Extracts and calculates areas from polygon geometries
- **🤖 Auto parameter estimation** - Automatically estimates cutoff and beta values
- **📊 Interactive visualization** - Generates frequency-area distribution plots
- **📈 Uncertainty analysis** - Optional Monte Carlo uncertainty estimation
- **🌍 CRS handling** - Automatic coordinate system detection and reprojection

---

## 🚀 Quick Start

### Option 1: Using the Setup Script (Recommended)

```bash
cd /Users/kdahal3/Desktop/pyslide-mLS
./run.sh
```

The script will:
1. Create a virtual environment
2. Install all dependencies
3. Launch the Flask application

Then open your browser to: **http://localhost:5000**

### Option 2: Manual Installation

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

---

## 📋 Requirements

- **Python 3.8+**
- See `requirements.txt` for package dependencies

### System Dependencies (for GeoPandas)

**macOS:**
```bash
brew install gdal
```

**Ubuntu/Debian:**
```bash
sudo apt-get install gdal-bin libgdal-dev
```

---

## 💻 Usage

### 1. Prepare Your Shapefile

Your shapefile should:
- Contain **polygon features** (landslide boundaries)
- Include all required files: `.shp`, `.shx`, `.dbf`, `.prj`
- Have a defined **coordinate reference system (CRS)**
- Be compressed as a **ZIP file** for upload

### 2. Upload and Analyze

1. **Start the application** (see Quick Start)
2. **Navigate to** http://localhost:5000
3. **Upload your shapefile ZIP**
4. **Optional:** Enter power-law parameters (or leave blank for auto-estimation)
5. **Click "Calculate mLS"**

### 3. View Results

The results page shows:
- **mLS value** with uncertainty
- **Frequency-area distribution plot**
- **Power-law parameters** (cutoff and beta)
- **Statistical summary** (total area, mean, median, etc.)

---

## 📊 Example Output

For a typical landslide inventory:

```
mLS = 3.63 ± 0.08
β = -2.46
Cutoff = 500 m²
Total landslides: 1,234
Total area: 1.5×10⁶ m²
```

The plot shows:
- Blue circles: Observed frequency density
- Red line: Power-law fit

---

## 🔧 Project Structure

```
pyslide-mLS/
├── app.py                      # Flask web application
├── mls_calculator.py           # Python conversion of mLS.m
├── powerlaw_estimator.py       # Parameter estimation
├── requirements.txt            # Python dependencies
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   └── about.html
├── run.sh                      # Quick start script
├── test_installation.py        # Test script
├── PYTHON_SETUP.md            # Detailed setup guide
├── mLS.m                       # Original MATLAB code (unchanged)
└── README_PYTHON.md           # This file
```

---

## 🧪 Testing

Run the test script to verify installation:

```bash
python test_installation.py
```

This will test:
- Package imports
- mLS calculator functionality
- Power-law parameter estimation

---

## 📚 Methodology

The mLS calculator uses the method from:

> **Tanyas, H., Allstadt, K.E., and van Westen, C.J., 2018.**  
> An updated method for estimating landslide-event magnitude.  
> *Earth Surface Processes and Landforms*, 43(9), pp.1836-1847.  
> DOI: [10.1002/esp.4359](https://doi.org/10.1002/esp.4359)

### Key Concepts

- **Power-Law Distribution:** Landslide sizes often follow: `p(A) ∝ A^β`
- **Cutoff (xmin):** Minimum area where power-law behavior begins
- **Beta (β):** Power-law exponent (typically -1.4 to -3.4)
- **mLS:** Logarithmic magnitude scale, similar to earthquake scales

For more details, visit the **About** page in the web application.

---

## 🎓 Citation

If you use this tool in your research, please cite:

```bibtex
@article{tanyas2018updated,
  title={An updated method for estimating landslide-event magnitude},
  author={Tanyas, Hakan and Allstadt, Kate E and van Westen, Cees J},
  journal={Earth Surface Processes and Landforms},
  volume={43},
  number={9},
  pages={1836--1847},
  year={2018},
  publisher={Wiley Online Library},
  doi={10.1002/esp.4359}
}
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### GDAL Installation Issues

See [PYTHON_SETUP.md](PYTHON_SETUP.md) for detailed GDAL installation instructions.

### Shapefile Upload Fails

Ensure your ZIP contains:
- `.shp` (geometry)
- `.shx` (shape index)
- `.dbf` (attributes)
- `.prj` (projection)

### Memory Issues with Large Shapefiles

For very large inventories (>10,000 features), consider:
- Increasing Flask's max content length
- Processing in batches
- Using a more powerful server

---

## 🔒 Security Note

This is a **research tool** intended for local use or trusted environments. For production deployment:

1. Change the Flask secret key
2. Use a production WSGI server (e.g., Gunicorn)
3. Implement proper authentication
4. Add input validation and sanitization
5. Use HTTPS

---

## 📝 License

See `LICENSE.md` in the repository root.

The original MATLAB code is from Tanyas et al. (2018) and is provided as supplementary material to their paper.

---

## 🤝 Contributing

This Python implementation aims to make the mLS method more accessible. The original MATLAB code (`mLS.m`) remains **unchanged**.

Contributions to improve the Python implementation are welcome:
- Bug fixes
- Performance improvements
- Additional features (e.g., batch processing, API endpoints)
- Documentation improvements

---

## 📧 Support

For questions about:
- **Methodology:** Refer to Tanyas et al. (2018)
- **Python implementation:** Check [PYTHON_SETUP.md](PYTHON_SETUP.md)
- **Original MATLAB code:** See the original [README.md](README.md)

---

## 🌟 Acknowledgments

- **Original Method:** Hakan Tanyas, Kate E. Allstadt, Cees J. van Westen
- **Python Implementation:** Conversion of MATLAB code to Python/Flask
- **Power-Law Estimation:** Based on methods from Clauset et al. (2009)

---

## 📖 Additional Resources

- [Detailed Setup Guide (PYTHON_SETUP.md)](PYTHON_SETUP.md)
- [Original MATLAB README (README.md)](README.md)
- [Original Paper](https://doi.org/10.1002/esp.4359)
- [Power-Law Methods](https://doi.org/10.1137/070710111)

---

**Made with ❤️ for the landslide research community**
