# pyslide-mLS

**Python implementation of the landslide-event magnitude scale (mLS) calculator with web interface**

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/license-Public%20Domain-green.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-lightgrey.svg)

---

## Overview

This repository provides both MATLAB and Python implementations for estimating landslide-event magnitude (mLS) from landslide inventory shapefiles. The Python version includes a Flask web interface for browser-based analysis.

**Reference:** Tanyas, H., K.E. Allstadt, and C.J. van Westen, 2018. An updated method for estimating landslide-event magnitude. *Earth Surface Processes and Landforms*. DOI: [10.1002/esp.4359](https://doi.org/10.1002/esp.4359)

## What is mLS?

mLS (landslide-event magnitude scale) quantifies the overall size/severity of a landslide event, similar to earthquake magnitude scales. It's calculated from the frequency-area distribution of landslides using power-law statistics.

## Quick Start

### Web Application (Python)

#### Linux/macOS:
```bash
git clone https://github.com/geokshitij/pyslide-mLS.git
cd pyslide-mLS
chmod +x run.sh
./run.sh
```

#### Windows:
```cmd
git clone https://github.com/geokshitij/pyslide-mLS.git
cd pyslide-mLS
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5001` in your browser and upload a shapefile ZIP.

### Manual Installation

#### Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### Windows (Command Prompt):
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**Note for Windows PowerShell users:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Features

- Browser-based interface for easy shapefile analysis
- **Dual parameter estimation methods**:
  - **Official**: Clauset et al. (2009) implementation via `powerlaw` package (recommended for research)
  - **Simplified**: Fast KS-based estimation (good for quick analysis)
  - **Auto**: Automatically uses official method if available, otherwise simplified
- Monte Carlo uncertainty quantification (10,000 iterations)
- Support for multiple shapefiles in one ZIP
- Automatic CRS handling and area calculation

## Repository Structure

```
pyslide-mLS/
├── app.py                  # Flask web application
├── mls_calculator.py       # Core mLS calculation
├── powerlaw_estimator.py   # Parameter estimation
├── templates/              # HTML templates
├── matlab_original/        # Original MATLAB code
├── tests/                  # Test scripts and data
└── docs/                   # Documentation
```

## Usage

### Web Interface

1. Upload your landslide inventory shapefile (as ZIP with .shp, .shx, .dbf, .prj)
2. Select shapefile if multiple exist in ZIP
3. View results: mLS value, uncertainty, power-law parameters, and plots

### Python Module

```python
from mls_calculator import calculate_mls
from powerlaw_estimator import estimate_powerlaw_parameters
import geopandas as gpd

gdf = gpd.read_file('landslides.shp')
areas = gdf.geometry.area.values

# Option 1: Auto method (recommended) - uses official if available
cutoff, beta, cutoff_error, beta_error, method = estimate_powerlaw_parameters(areas, method='auto')

# Option 2: Force official Clauset et al. (2009) method
cutoff, beta, cutoff_error, beta_error, method = estimate_powerlaw_parameters(areas, method='official')

# Option 3: Force simplified method (faster)
cutoff, beta, cutoff_error, beta_error, method = estimate_powerlaw_parameters(areas, method='simplified')

mls, uncertainty, plot = calculate_mls(areas, cutoff, beta, beta_error, cutoff_error)

print(f"mLS = {mls:.2f} ± {uncertainty:.2f}")
print(f"Parameters estimated using {method} method")
```

### MATLAB

```matlab
load('matlab_original/sample_data.mat');
load('matlab_original/beta.mat');
load('matlab_original/cutoff.mat');
load('matlab_original/beta_error.mat');
load('matlab_original/cutoff_error.mat');

[mLS_value, error] = mLS(Area, cutoff, beta, beta_error, cutoff_error);
fprintf('mLS = %.2f ± %.2f\n', mLS_value, error);
```

## Requirements

**Python:**
- Python 3.9+
- Flask 3.0.0
- GeoPandas 1.1.1
- NumPy, Matplotlib, SciPy
- See `requirements.txt`

**MATLAB:**
- MATLAB R2015b+
- No additional toolboxes

## Methodology

1. Load landslide areas from shapefile polygons
2. Estimate power-law parameters (see **Parameter Estimation** below)
3. Calculate frequency-area distribution with logarithmic bins
4. Fit power-law to medium/large landslides (above cutoff)
5. Compute mLS using reference inventory (1994 Northridge)
6. Quantify uncertainty via Monte Carlo simulation

### Parameter Estimation Methods

This tool offers three methods for estimating power-law parameters (cutoff and beta):

#### 1. Official Method (Recommended for Research)
Uses the [`powerlaw`](https://github.com/jeffalstott/powerlaw) package by Alstott et al., which implements the full Clauset et al. (2009) methodology:
- Maximum likelihood estimation with proper goodness-of-fit tests
- Bootstrap-based uncertainty quantification
- Rigorous statistical validation
- **When to use**: Publication-quality analysis, research papers, detailed studies
- **Speed**: Slower (~10-30 seconds for 1000 landslides)

#### 2. Simplified Method (Fast)
Simplified KS-based implementation:
- Grid search over cutoff candidates
- MLE for beta: `beta = 1 + n / sum(ln(x/xmin))`
- Kolmogorov-Smirnov test for goodness-of-fit
- Approximate error estimation
- **When to use**: Quick exploratory analysis, field work, rapid assessments
- **Speed**: Fast (~1-2 seconds for 1000 landslides)

#### 3. Auto Method (Default)
Automatically uses the official method if the `powerlaw` package is installed, otherwise falls back to simplified method. This is the default and recommended for most users.

**Reference**: Clauset, A., Shalizi, C.R., and Newman, M.E.J. (2009). "Power-law distributions in empirical data." *SIAM Review*, 51(4), 661-703.

## Interpretation

**mLS Scale** (based on Tanyas et al. 2018 database of 45 earthquake-induced landslide inventories):

| mLS Range | Example Events | Typical # Landslides | Total Area | Description |
|-----------|----------------|---------------------|------------|-------------|
| < 2.5 | Loma Prieta (1989), Niigata Chuetsu-Oki (2007) | 100-600 | < 1 km² | Small localized events |
| 2.5-3.5 | Friuli (1976), Coalinga (1983), Pisco (2007) | 200-4,000 | 1-10 km² | Small to moderate events |
| 3.5-4.5 | Mid-Niigata (2004), Northridge (1994) | 1,000-11,000 | 10-40 km² | Moderate to large events |
| 4.5-5.5 | Guatemala (1976), Denali (2002), Kashmir (2005) | 1,500-6,200 | 50-200 km² | Large regional events |
| > 5.5 | Wenchuan (2008), Chi-chi (1999) | 60,000-200,000 | 500-1200 km² | Very large/catastrophic events |

**Note:** These categories are interpretive based on the distribution of events in Tanyas et al. (2018). The paper does not explicitly define verbal magnitude categories.

**Beta (β):** Power-law exponent (typically -1.4 to -3.4)
- Controls the relative frequency of large vs. small landslides
- Steeper (more negative) = fewer very large landslides

**Cutoff:** Inventory completeness threshold
- Minimum landslide area where power-law behavior begins
- Below this, undersampling or different processes dominate

## Testing

**Linux/macOS:**
```bash
python tests/test_matlab_comparison.py
python tests/test_installation.py
```

**Windows:**
```cmd
python tests\test_matlab_comparison.py
python tests\test_installation.py
```

Expected output with sample data:
- mLS: 3.6273
- Uncertainty: ±0.0846

## Troubleshooting

### Windows-Specific Issues

**1. Python not found:**
- Install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation
- Restart Command Prompt/PowerShell after installation

**2. PowerShell execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**3. GDAL/Fiona installation fails:**
If you get errors installing `geopandas` or `fiona`, try:
```cmd
pip install pipwin
pipwin install gdal
pipwin install fiona
pip install -r requirements.txt
```

Or use conda (recommended for Windows):
```cmd
conda create -n mls python=3.11
conda activate mls
conda install -c conda-forge geopandas flask matplotlib scipy powerlaw
python app.py
```

**4. Virtual environment activation issues:**
- Command Prompt: `venv\Scripts\activate.bat`
- PowerShell: `venv\Scripts\Activate.ps1`
- Git Bash: `source venv/Scripts/activate`

### General Issues

**Port 5001 already in use:**
Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Changed from 5001
```

**Out of memory errors:**
Reduce Monte Carlo iterations in `mls_calculator.py`:
```python
n_iterations = 1000  # Default is 10000
```

## References

- Tanyas, H., et al., 2018. An updated method for estimating landslide-event magnitude. *Earth Surface Processes and Landforms*, 43(9), 1836-1847.
- Clauset, A., et al., 2009. Power-law distributions in empirical data. *SIAM Review*, 51(4), 661-703.

## Contributing

Contributions welcome! Please submit Pull Requests or open Issues.

## License

Public domain for research and educational purposes. See LICENSE.md and DISCLAIMER.md.

## Acknowledgments

- Original MATLAB: Hakan Tanyaş, Kate E. Allstadt, Cees J. van Westen
- Python implementation and web interface
- USGS Landslide Hazards Program

## Contact

- GitHub Issues: [github.com/geokshitij/pyslide-mLS/issues](https://github.com/geokshitij/pyslide-mLS/issues)
- Citation: Please cite Tanyas et al. (2018)

---

**Made for the landslide research community**
