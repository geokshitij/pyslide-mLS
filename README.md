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

```bash
git clone https://github.com/geokshitij/pyslide-mLS.git
cd pyslide-mLS
chmod +x run.sh
./run.sh
```

Then open `http://localhost:5001` in your browser and upload a shapefile ZIP.

### Manual Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
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

**mLS Scale:**
- < 2.0: Small event
- 2.0-3.5: Moderate event
- 3.5-5.0: Large event
- \> 5.0: Major/catastrophic event

**Beta (β):** Power-law exponent (typically -1.4 to -3.4)

**Cutoff:** Inventory completeness threshold

## Testing

```bash
python tests/test_matlab_comparison.py
python tests/test_installation.py
```

Expected output with sample data:
- mLS: 3.6273
- Uncertainty: ±0.0846

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
