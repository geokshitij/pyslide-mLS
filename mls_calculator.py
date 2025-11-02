"""
Python conversion of the mLS (landslide magnitude) calculation method.

This script is a Python implementation of the MATLAB code from:
Tanyas, H., K.E. Allstadt, and C.J. van Westen, 2018, 
An updated method for estimating landslide-event magnitude, Earth Surface 
Processes and Landforms. DOI: 10.1002/esp.4359

The original MATLAB code has not been modified. This is a new Python implementation.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web server
import matplotlib.pyplot as plt
from scipy import stats
import io
import base64


def calculate_mls(area, cutoff, beta, beta_error=None, cutoff_error=None):
    """
    Calculate landslide-event magnitude (mLS).
    
    Parameters:
    -----------
    area : array-like
        Landslide areas in square meters
    cutoff : float
        Smallest area that follows power law (in square meters)
    beta : float
        Power-law exponent (scaling parameter)
    beta_error : float, optional
        Uncertainty in beta value
    cutoff_error : float, optional
        Uncertainty in cutoff value
        
    Returns:
    --------
    mls_value : float
        Landslide-event magnitude
    error : float or str
        Uncertainty in mLS (or '?' if not calculated)
    plot_base64 : str
        Base64 encoded plot image
    """
    
    # Convert area to numpy array
    area = np.array(area)
    
    # Define bins with increasing sizes
    x1 = np.zeros(120)
    x1[0] = 2
    for i in range(1, 120):
        x1[i] = x1[i-1] * 1.2
    
    # Calculate frequency for each bin
    freq = np.histogram(area, bins=x1)[0]
    
    # Calculate bin intervals
    internal = np.zeros(len(x1) - 1)
    for i in range(len(internal)):
        if i == 0:
            internal[i] = x1[0]
        else:
            internal[i] = x1[i] - x1[i-1]
    
    # Calculate frequency density
    fd = freq / internal
    
    # Use bin centers for x1 (for plotting consistency with MATLAB)
    x1_centers = np.zeros(len(x1) - 1)
    for i in range(len(x1_centers)):
        x1_centers[i] = (x1[i] + x1[i+1]) / 2
    x1 = x1_centers
    
    # Find index closest to cutoff value
    x1_rev = np.abs(x1 - cutoff)
    index_midpoint = np.argmin(x1_rev)
    
    # Define x and y arrays for frequency-size distribution
    x = x1[index_midpoint:]
    y = fd[index_midpoint:]
    
    # Beta value must be negative
    if beta > 0:
        beta = -1 * beta
    beta_stored = beta
    
    # Calculate constant along the power-law where x=cutoff
    constant = y[0] / (cutoff ** beta)
    
    # Calculate frequency-density values for power-law fit
    fit_y = constant * (x1 ** beta)
    fit_y_stored = fit_y.copy()
    
    # Calculate midpoint values
    midx = 10 ** ((np.log10(max(area)) + np.log10(cutoff)) / 2)
    midy = constant * (midx ** beta)
    
    # Reference values from Northridge inventory
    ref_midx = 4.876599623713225e+04
    ref_midy = 8.364725347860417e-04
    ac = ref_midy / (11111 * (ref_midx ** beta))
    
    # Calculate mLS
    mls_value = np.log10(midy / (ac * (midx ** beta)))
    mls_stored = mls_value
    
    # Calculate uncertainty if error parameters provided
    error = '?'
    if beta_error is not None and cutoff_error is not None:
        # Create arrays of uniformly distributed beta and cutoff values
        beta_interval = np.linspace(beta_stored - beta_error, 
                                   beta_stored + beta_error, 500)
        
        cutoff_min = max(cutoff - cutoff_error, 2)
        cutoff_max = cutoff + cutoff_error
        cutoff_interval = np.linspace(cutoff_min, cutoff_max, 500)
        
        beta_mean = np.mean(beta_interval)
        beta_std = np.std(beta_interval)
        cutoff_mean = np.mean(cutoff_interval)
        cutoff_std = np.std(cutoff_interval)
        
        # Monte Carlo simulation (10,000 iterations)
        mls_array = []
        for _ in range(10000):
            cutoff_sim = np.random.normal(cutoff_mean, cutoff_std)
            beta_sim = np.random.normal(beta_mean, beta_std)
            
            constant_sim = y[0] / (cutoff_sim ** beta_sim)
            midx_sim = 10 ** ((np.log10(max(area)) + np.log10(cutoff_sim)) / 2)
            ac_sim = ref_midy / (11111 * (ref_midx ** beta_sim))
            mls_sim = np.log10(midy / (ac_sim * (midx_sim ** beta_sim)))
            
            if not np.isinf(mls_sim):
                mls_array.append(mls_sim)
        
        error = np.std(mls_array)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Plot all frequency density points (blue circles)
    ax.loglog(x1, fd, 'o', markersize=5, markerfacecolor='b', 
              markeredgecolor='k', label='Observed data density')
    
    # Plot power-law fit ONLY in the power-law region (from cutoff onwards)
    # Create x values for the fit line from cutoff to max area
    x_fit = x1[x1 >= cutoff]
    y_fit = constant * (x_fit ** beta_stored)
    ax.loglog(x_fit, y_fit, '-', linewidth=2, color='r', label='Fitted distribution')
    
    ax.set_xlim([1, 1e7])
    ax.set_ylim([1e-6, 1000])
    ax.set_xlabel('Landslide Area (m²)', fontsize=12, fontweight='normal')
    ax.set_ylabel('Probability Density (m⁻²)', fontsize=12, fontweight='normal')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    
    # Add text with beta and mLS values
    if isinstance(error, str):
        text_str = f'β = {beta_stored:.2f}\nmLS = {mls_stored:.2f} ± {error}'
    else:
        text_str = f'β = {beta_stored:.2f}\nmLS = {mls_stored:.2f} ± {error:.2f}'
    
    # Position text at bottom left
    fd_nonzero = fd[fd > 0]
    if len(fd_nonzero) > 0:
        y_pos = min(fd_nonzero) * 10
    else:
        y_pos = 1e-5
    ax.text(x1[0], y_pos, text_str, fontsize=12, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    plot_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()
    
    return mls_stored, error, plot_base64


if __name__ == "__main__":
    # Test with sample data if available
    print("mLS Calculator - Python Implementation")
    print("This module provides landslide magnitude calculation functionality.")
