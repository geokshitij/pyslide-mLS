"""
Power-law parameter estimation for landslide frequency-area distributions.

This module provides functionality to estimate cutoff and beta parameters
using methods similar to Clauset et al. (2009).
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar


def estimate_powerlaw_parameters(areas, xmin_range=None):
    """
    Estimate power-law parameters (cutoff and beta) for area distribution.
    
    This is a simplified implementation. For more accurate results, use
    the methods from Clauset et al. (2009).
    
    Parameters:
    -----------
    areas : array-like
        Landslide areas in square meters
    xmin_range : tuple, optional
        (min, max) range for cutoff search
        
    Returns:
    --------
    cutoff : float
        Estimated cutoff value (xmin)
    beta : float
        Estimated power-law exponent
    cutoff_error : float
        Estimated error in cutoff
    beta_error : float
        Estimated error in beta
    """
    
    areas = np.array(areas)
    areas = areas[areas > 0]  # Remove zero or negative values
    areas = np.sort(areas)
    
    if xmin_range is None:
        # Search between 10th percentile and median
        xmin_range = (np.percentile(areas, 10), np.percentile(areas, 50))
    
    best_cutoff = None
    best_beta = None
    best_ks = float('inf')
    
    # Try different cutoff values
    cutoff_candidates = np.linspace(xmin_range[0], xmin_range[1], 50)
    
    for cutoff in cutoff_candidates:
        # Filter data above cutoff
        data = areas[areas >= cutoff]
        
        if len(data) < 50:  # Need enough data points
            continue
        
        # Estimate beta using maximum likelihood
        # For discrete power law: beta = 1 + n / sum(ln(x/xmin))
        n = len(data)
        if np.all(data > 0):
            beta_est = 1 + n / np.sum(np.log(data / cutoff))
            
            # Make beta negative (as used in the mLS code)
            beta_est = -abs(beta_est)
            
            # Calculate KS statistic
            # Generate theoretical CDF
            x_theory = np.linspace(cutoff, max(data), 1000)
            # For power law: P(X >= x) = (x/xmin)^(-alpha) where alpha = beta - 1
            alpha = abs(beta_est) - 1
            cdf_theory = 1 - (x_theory / cutoff) ** (-alpha)
            
            # Empirical CDF
            empirical_cdf = np.searchsorted(data, x_theory, side='right') / len(data)
            
            # KS statistic
            ks = np.max(np.abs(cdf_theory - empirical_cdf))
            
            if ks < best_ks:
                best_ks = ks
                best_cutoff = cutoff
                best_beta = beta_est
    
    # If no good fit found, use simple heuristics
    if best_cutoff is None or best_beta is None:
        best_cutoff = np.percentile(areas, 25)
        
        # Estimate beta from log-log slope
        data = areas[areas >= best_cutoff]
        
        # Create bins
        bins = np.logspace(np.log10(best_cutoff), np.log10(max(data)), 30)
        hist, bin_edges = np.histogram(data, bins=bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Remove zero frequencies
        mask = hist > 0
        x_fit = np.log10(bin_centers[mask])
        y_fit = np.log10(hist[mask])
        
        if len(x_fit) > 5:
            slope, intercept = np.polyfit(x_fit, y_fit, 1)
            best_beta = slope  # Slope is approximately beta
        else:
            best_beta = -2.3  # Default value from literature
    
    # Estimate errors (simplified approach)
    # In practice, use bootstrap or methods from Clauset et al.
    data = areas[areas >= best_cutoff]
    n = len(data)
    
    # Standard error for beta (approximate)
    beta_error = abs(best_beta - 1) / np.sqrt(n)
    
    # Error for cutoff (use ~10% of cutoff as rough estimate)
    cutoff_error = best_cutoff * 0.1
    
    return best_cutoff, best_beta, cutoff_error, beta_error


if __name__ == "__main__":
    # Test with synthetic data
    print("Power-law Parameter Estimator")
    print("This module provides automatic estimation of cutoff and beta parameters.")
    
    # Generate synthetic power-law data for testing
    np.random.seed(42)
    true_beta = -2.3
    true_cutoff = 100
    n_samples = 1000
    
    # Generate power-law distributed data
    u = np.random.uniform(0, 1, n_samples)
    alpha = abs(true_beta) - 1
    synthetic_areas = true_cutoff * (1 - u) ** (-1/alpha)
    
    cutoff_est, beta_est, cutoff_err, beta_err = estimate_powerlaw_parameters(synthetic_areas)
    
    print(f"\nTest with synthetic data:")
    print(f"True cutoff: {true_cutoff}, Estimated: {cutoff_est:.2f} ± {cutoff_err:.2f}")
    print(f"True beta: {true_beta}, Estimated: {beta_est:.2f} ± {beta_err:.2f}")
