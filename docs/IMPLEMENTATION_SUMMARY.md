# Python Flask Implementation Summary

## Overview

This document summarizes the Python Flask web application created for the mLS (landslide-event magnitude) calculator. The original MATLAB code (`mLS.m`) has **NOT been modified** and remains in the repository unchanged.

## What Was Created

### Core Python Files

1. **`mls_calculator.py`**
   - Python conversion of the MATLAB `mLS.m` function
   - Implements all mathematical calculations from the original
   - Generates matplotlib plots (converted from MATLAB plotting)
   - Returns mLS value, error estimate, and base64-encoded plot

2. **`powerlaw_estimator.py`**
   - Automatic estimation of power-law parameters (cutoff and beta)
   - Based on methods similar to Clauset et al. (2009)
   - Provides fallback when users don't have pre-calculated values

3. **`app.py`**
   - Flask web application with routes
   - Handles file upload (shapefile ZIP files)
   - Processes shapefiles using GeoPandas
   - Calculates areas from polygon geometries
   - Handles CRS transformations (geographic to projected)
   - Integrates with mLS calculator
   - Serves HTML templates

### Web Templates (in `templates/`)

4. **`base.html`**
   - Base template with layout, header, navigation, footer
   - Responsive design with gradient styling
   - Flash message handling

5. **`index.html`**
   - Upload form with drag-and-drop functionality
   - Optional parameter input fields
   - Instructions and help text
   - Client-side validation

6. **`results.html`**
   - Display mLS results with large prominent value
   - Embedded frequency-area distribution plot
   - Statistics grid (total area, mean, median, etc.)
   - Parameter table
   - Option to analyze another file

7. **`about.html`**
   - Methodology explanation
   - Parameter descriptions
   - References and citations
   - Usage guidelines

### Configuration & Setup Files

8. **`requirements.txt`**
   - Python package dependencies
   - Flask, GeoPandas, NumPy, Matplotlib, SciPy, etc.

9. **`run.sh`**
   - Convenience script for setup and launch
   - Creates virtual environment
   - Installs dependencies
   - Starts Flask application

10. **`test_installation.py`**
    - Automated testing of installation
    - Verifies all packages import correctly
    - Tests mLS calculation with synthetic data
    - Tests parameter estimation

11. **`.gitignore`**
    - Excludes Python cache files
    - Excludes virtual environment
    - Excludes uploaded files
    - Excludes IDE-specific files

### Documentation Files

12. **`PYTHON_SETUP.md`**
    - Comprehensive setup guide
    - Installation instructions for all platforms
    - Troubleshooting section
    - Usage examples
    - Configuration options

13. **`README_PYTHON.md`**
    - Main README for Python implementation
    - Quick start guide
    - Feature overview
    - Project structure
    - Citation information

14. **`QUICKSTART.md`**
    - Quick reference for common tasks
    - Command cheat sheet
    - Typical workflow
    - Troubleshooting quick fixes

### Directories Created

15. **`templates/`**
    - Contains all HTML templates

16. **`static/`**
    - For static assets (CSS, JS, images)
    - Currently empty, ready for future additions

## Key Features

### 1. Shapefile Processing
- Accepts ZIP files containing shapefile components
- Automatically extracts and reads shapefiles
- Validates required files (.shp, .shx, .dbf, .prj)
- Calculates polygon areas using GeoPandas

### 2. CRS Handling
- Detects coordinate reference system
- Automatically reprojects geographic coordinates to UTM
- Ensures accurate area calculations in square meters

### 3. Parameter Estimation
- Automatic estimation of cutoff and beta values
- Uses power-law fitting techniques
- Provides error estimates
- Optional: users can provide their own values

### 4. mLS Calculation
- Faithful implementation of Tanyas et al. (2018) method
- Monte Carlo uncertainty estimation (10,000 iterations)
- Reference to Northridge inventory
- Frequency-area distribution analysis

### 5. Visualization
- Matplotlib-based plotting
- Log-log frequency-area distribution
- Power-law fit overlay
- Base64 encoding for web display

### 6. User Interface
- Modern, responsive design
- Drag-and-drop file upload
- Interactive forms
- Real-time feedback
- Results visualization

## Technical Architecture

```
User Browser
    ↓
Flask Web Server (app.py)
    ↓
├─→ File Upload Handler
│   └─→ GeoPandas (shapefile processing)
│       └─→ Area calculation
│
├─→ Parameter Estimator (powerlaw_estimator.py)
│   └─→ Cutoff and beta estimation
│
└─→ mLS Calculator (mls_calculator.py)
    ├─→ NumPy (numerical operations)
    ├─→ SciPy (statistics)
    └─→ Matplotlib (plotting)
        └─→ Base64-encoded plot
            └─→ HTML Template Rendering
                └─→ User Browser
```

## Data Flow

1. **Upload**: User uploads shapefile ZIP
2. **Extract**: Flask extracts ZIP to temporary directory
3. **Read**: GeoPandas reads shapefile
4. **Transform**: CRS conversion if needed
5. **Calculate**: Areas computed from polygons
6. **Estimate**: Power-law parameters determined
7. **Compute**: mLS value calculated
8. **Plot**: Frequency-area distribution generated
9. **Display**: Results shown in web interface
10. **Cleanup**: Temporary files removed

## Comparison with MATLAB Code

| Aspect | MATLAB (`mLS.m`) | Python (`mls_calculator.py`) |
|--------|------------------|------------------------------|
| Language | MATLAB | Python |
| Interface | Function call | Web application |
| Input | Array variable | Shapefile upload |
| Area calculation | Manual | Automatic (from geometry) |
| Parameter estimation | External (plfit.m) | Built-in (optional) |
| Output | Plot window + variables | Web page + embedded plot |
| Plotting | MATLAB figure | Matplotlib (base64) |
| Uncertainty | Monte Carlo | Monte Carlo (same method) |

## Dependencies

### Python Packages
- Flask 3.0.0 - Web framework
- GeoPandas 0.14.1 - Spatial data processing
- NumPy 1.26.2 - Numerical operations
- Matplotlib 3.8.2 - Plotting
- SciPy 1.11.4 - Statistical functions
- Shapely 2.0.2 - Geometric operations
- Fiona 1.9.5 - Shapefile I/O
- pyproj 3.6.1 - Coordinate transformations

### System Dependencies
- Python 3.8+
- GDAL (for GeoPandas)

## Usage Scenarios

### Scenario 1: Quick Analysis
1. User has shapefile
2. Uploads ZIP
3. Leaves parameters blank (auto-estimate)
4. Gets mLS result immediately

### Scenario 2: Precise Analysis
1. User pre-calculates parameters using plfit.m
2. Uploads shapefile
3. Enters cutoff, beta, and errors
4. Gets mLS with accurate uncertainty

### Scenario 3: Batch Processing
1. Multiple inventories to analyze
2. Upload each one sequentially
3. Save/export results
4. Compare mLS values

## Future Enhancements (Not Implemented)

Potential additions:
- Batch processing multiple shapefiles
- CSV export of results
- API endpoints for programmatic access
- Database storage of results
- User accounts and history
- Comparison tools for multiple inventories
- Advanced parameter tuning interface

## Testing

### Automated Tests
- `test_installation.py` verifies:
  - Package imports
  - mLS calculation with synthetic data
  - Parameter estimation

### Manual Testing
1. Synthetic data generation
2. Known inventory comparison
3. Edge cases (small datasets, unusual distributions)

## Security Considerations

⚠️ **Note**: This is a research tool. For production:
- Change Flask secret key
- Use production WSGI server (Gunicorn/uWSGI)
- Implement authentication
- Add rate limiting
- Validate file types strictly
- Sanitize inputs
- Use HTTPS

## Maintenance

### Regular Updates
- Keep dependencies updated
- Monitor security advisories
- Test with new Python versions

### Known Limitations
- File size limited to 50MB (configurable)
- Single file upload at a time
- Synchronous processing (may timeout on very large files)

## Acknowledgments

### Original Method
- Hakan Tanyas
- Kate E. Allstadt  
- Cees J. van Westen

### Implementation
- Python conversion maintains fidelity to original MATLAB code
- Web interface makes method accessible without MATLAB license
- Automatic shapefile processing simplifies workflow

## Citation

Users of this tool should cite:

```
Tanyas, H., K.E. Allstadt, and C.J. van Westen, 2018, 
An updated method for estimating landslide-event magnitude, 
Earth Surface Processes and Landforms. DOI: 10.1002/esp.4359
```

## Files Not Modified

The following original files remain **unchanged**:
- `mLS.m` - Original MATLAB function
- `README.md` - Original README
- `LICENSE.md` - Original license
- `DISCLAIMER.md` - Original disclaimer
- All `.mat` files - Sample data and parameters

## Conclusion

This Python Flask implementation provides:
- ✅ Complete functionality of original MATLAB code
- ✅ User-friendly web interface
- ✅ Automatic shapefile processing
- ✅ Cross-platform compatibility
- ✅ No MATLAB license required
- ✅ Open-source Python ecosystem
- ✅ Extensible architecture

The implementation is ready for use in research and education, maintaining the scientific integrity of the original method while improving accessibility.
