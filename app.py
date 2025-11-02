"""
Flask web application for landslide magnitude (mLS) calculation.
Allows users to upload shapefiles and calculate mLS values.
"""

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
import os
import geopandas as gpd
import numpy as np
from werkzeug.utils import secure_filename
import zipfile
import tempfile
import shutil
from mls_calculator import calculate_mls
from powerlaw_estimator import estimate_powerlaw_parameters

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production-' + os.urandom(24).hex()
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

ALLOWED_EXTENSIONS = {'zip', 'shp', 'dbf', 'shx', 'prj'}


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_shapefile(zip_path, extract_dir):
    """Extract shapefile from zip archive and return list of .shp files."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Find all .shp files (including in subdirectories)
    shp_files = []
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith('.shp'):
                # Store relative path from extract_dir
                rel_path = os.path.relpath(os.path.join(root, file), extract_dir)
                shp_files.append(rel_path)
    
    if not shp_files:
        raise ValueError("No .shp file found in the uploaded zip")
    
    return shp_files


def calculate_areas_from_shapefile(shapefile_path):
    """
    Read shapefile and calculate areas of polygons.
    
    Parameters:
    -----------
    shapefile_path : str
        Path to the shapefile
        
    Returns:
    --------
    areas : array
        Array of polygon areas in square meters
    """
    # Read shapefile
    gdf = gpd.read_file(shapefile_path)
    
    # Ensure geometry is valid
    gdf['geometry'] = gdf['geometry'].buffer(0)
    
    # Check if CRS is projected (for accurate area calculation)
    if gdf.crs is None:
        raise ValueError("Shapefile has no coordinate reference system (CRS) defined")
    
    # If CRS is geographic (lat/lon), reproject to appropriate UTM zone
    if gdf.crs.is_geographic:
        # Get the centroid of all features to determine UTM zone
        centroid = gdf.dissolve().centroid.iloc[0]
        lon = centroid.x
        
        # Calculate UTM zone
        utm_zone = int((lon + 180) / 6) + 1
        hemisphere = 'north' if centroid.y >= 0 else 'south'
        
        # Create UTM CRS
        utm_crs = f"+proj=utm +zone={utm_zone} +{hemisphere} +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
        
        # Reproject
        gdf = gdf.to_crs(utm_crs)
        flash(f'Shapefile reprojected to UTM Zone {utm_zone}{hemisphere[0].upper()} for area calculation', 'info')
    
    # Calculate areas in square meters
    areas = gdf.geometry.area.values
    
    # Filter out very small polygons (< 1 m²)
    areas = areas[areas >= 1]
    
    return areas, len(gdf), gdf.crs


@app.route('/')
def index():
    """Render the main upload page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process shapefile."""
    if 'shapefile' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    
    file = request.files['shapefile']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a ZIP file containing shapefile components', 'error')
        return redirect(url_for('index'))
    
    try:
        # Create temporary directory for this upload
        temp_dir = tempfile.mkdtemp()
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        
        # Extract if zip file
        if filename.endswith('.zip'):
            extract_dir = os.path.join(temp_dir, 'extracted')
            os.makedirs(extract_dir, exist_ok=True)
            shp_files = extract_shapefile(filepath, extract_dir)
            
            # If multiple shapefiles found, show selection page
            if len(shp_files) > 1:
                # Store temp directory path in session
                session['temp_dir'] = temp_dir
                session['extract_dir'] = extract_dir
                return render_template('select_shapefile.html', 
                                     shapefiles=shp_files,
                                     original_params=request.form.to_dict())
            
            # Single shapefile found
            shapefile_path = os.path.join(extract_dir, shp_files[0])
        else:
            shapefile_path = filepath
        
        # Calculate areas from shapefile
        areas, feature_count, crs = calculate_areas_from_shapefile(shapefile_path)
        
        if len(areas) == 0:
            flash('No valid polygons found in shapefile', 'error')
            shutil.rmtree(temp_dir)
            return redirect(url_for('index'))
        
        # Get user-provided parameters or estimate them
        cutoff = request.form.get('cutoff', type=float)
        beta = request.form.get('beta', type=float)
        beta_error = request.form.get('beta_error', type=float)
        cutoff_error = request.form.get('cutoff_error', type=float)
        estimation_method = request.form.get('estimation_method', 'auto')
        
        # If parameters not provided, estimate them
        method_used = None
        if cutoff is None or beta is None:
            method_name = {'auto': 'automatic', 'official': 'Clauset et al. (2009)', 'simplified': 'simplified'}
            flash(f'Estimating power-law parameters using {method_name.get(estimation_method, "automatic")} method...', 'info')
            estimated_cutoff, estimated_beta, est_cutoff_err, est_beta_err, method_used = estimate_powerlaw_parameters(areas, method=estimation_method)
            flash(f'Parameters estimated using {method_used} method', 'success')
            
            if cutoff is None:
                cutoff = estimated_cutoff
            if beta is None:
                beta = estimated_beta
            if beta_error is None:
                beta_error = est_beta_err
            if cutoff_error is None:
                cutoff_error = est_cutoff_err
        
        # Calculate mLS
        mls_value, error, plot_base64 = calculate_mls(
            areas, cutoff, beta, beta_error, cutoff_error
        )
        
        # Prepare results
        results = {
            'mls': float(mls_value),
            'error': float(error) if isinstance(error, (int, float)) else error,
            'beta': float(beta),
            'cutoff': float(cutoff),
            'beta_error': float(beta_error) if beta_error is not None else None,
            'cutoff_error': float(cutoff_error) if cutoff_error is not None else None,
            'estimation_method': method_used,
            'feature_count': int(feature_count),
            'valid_areas_count': int(len(areas)),
            'min_area': float(np.min(areas)),
            'max_area': float(np.max(areas)),
            'mean_area': float(np.mean(areas)),
            'median_area': float(np.median(areas)),
            'total_area': float(np.sum(areas)),
            'crs': str(crs),
            'plot': plot_base64,
            'shapefile_name': os.path.basename(shapefile_path) if isinstance(shapefile_path, str) else filename
        }
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        return render_template('results.html', results=results)
        
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
        return redirect(url_for('index'))


@app.route('/process_selected', methods=['POST'])
def process_selected():
    """Process the selected shapefile from multiple options."""
    selected_shp = request.form.get('selected_shapefile')
    temp_dir = session.get('temp_dir')
    extract_dir = session.get('extract_dir')
    
    if not selected_shp or not temp_dir or not extract_dir:
        flash('Invalid selection or session expired', 'error')
        return redirect(url_for('index'))
    
    try:
        shapefile_path = os.path.join(extract_dir, selected_shp)
        
        if not os.path.exists(shapefile_path):
            flash('Selected shapefile not found', 'error')
            shutil.rmtree(temp_dir, ignore_errors=True)
            return redirect(url_for('index'))
        
        # Get parameters from form
        cutoff = request.form.get('cutoff', type=float)
        beta = request.form.get('beta', type=float)
        beta_error = request.form.get('beta_error', type=float)
        cutoff_error = request.form.get('cutoff_error', type=float)
        
        # Calculate areas and process
        areas, feature_count, crs = calculate_areas_from_shapefile(shapefile_path)
        
        if len(areas) == 0:
            flash('No valid polygons found in shapefile', 'error')
            shutil.rmtree(temp_dir)
            return redirect(url_for('index'))
        
        # Get estimation method
        estimation_method = request.form.get('estimation_method', 'auto')
        
        # Estimate parameters if not provided
        method_used = None
        if cutoff is None or beta is None:
            method_name = {'auto': 'automatic', 'official': 'Clauset et al. (2009)', 'simplified': 'simplified'}
            flash(f'Estimating power-law parameters using {method_name.get(estimation_method, "automatic")} method...', 'info')
            estimated_cutoff, estimated_beta, est_cutoff_err, est_beta_err, method_used = estimate_powerlaw_parameters(areas, method=estimation_method)
            flash(f'Parameters estimated using {method_used} method', 'success')
            
            if cutoff is None:
                cutoff = estimated_cutoff
            if beta is None:
                beta = estimated_beta
            if beta_error is None:
                beta_error = est_beta_err
            if cutoff_error is None:
                cutoff_error = est_cutoff_err
        
        # Calculate mLS
        mls_value, error, plot_base64 = calculate_mls(
            areas, cutoff, beta, beta_error, cutoff_error
        )
        
        # Prepare results
        results = {
            'mls': float(mls_value),
            'error': float(error) if isinstance(error, (int, float)) else error,
            'beta': float(beta),
            'cutoff': float(cutoff),
            'beta_error': float(beta_error) if beta_error is not None else None,
            'cutoff_error': float(cutoff_error) if cutoff_error is not None else None,
            'estimation_method': method_used,
            'feature_count': int(feature_count),
            'valid_areas_count': int(len(areas)),
            'min_area': float(np.min(areas)),
            'max_area': float(np.max(areas)),
            'mean_area': float(np.mean(areas)),
            'median_area': float(np.median(areas)),
            'total_area': float(np.sum(areas)),
            'crs': str(crs),
            'plot': plot_base64,
            'shapefile_name': selected_shp
        }
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        # Clear session
        session.pop('temp_dir', None)
        session.pop('extract_dir', None)
        
        return render_template('results.html', results=results)
        
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        # Clear session
        session.pop('temp_dir', None)
        session.pop('extract_dir', None)
        return redirect(url_for('index'))


@app.route('/about')
def about():
    """Render the about page with methodology information."""
    return render_template('about.html')


if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the app
    print("Starting mLS Calculator Flask Application")
    print("Navigate to http://localhost:5001 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5001)
