"""
Power-law parameter estimation for landslide frequency-area distributions.

This module provides functionality to estimate cutoff and beta parameters
using the official powerlaw package (Clauset et al. 2009 implementation)
with a simplified fallback method.
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar

# Try to import the official powerlaw package
try:
    import powerlaw
    POWERLAW_AVAILABLE = True
except ImportError:
    POWERLAW_AVAILABLE = False
    print("Warning: 'powerlaw' package not installed. Using simplified estimation method.")
    print("For more accurate results, install it with: pip install powerlaw")


def estimate_powerlaw_parameters_official(areas, xmin_range=None):
    """
    Estimate power-law parameters using the official powerlaw package.
    
    This uses the Clauset et al. (2009) methodology with proper
    bootstrap uncertainty estimation.
    
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
        Estimated power-law exponent (negative)
    cutoff_error : float
        Estimated error in cutoff
    beta_error : float
        Estimated error in beta
    method : str
        Method used ('official' or 'simplified')
    """
    areas = np.array(areas)
    areas = areas[areas > 0]
    areas_sorted = np.sort(areas)
    
    # Fit power-law using official package
    # Provide xmin search range - from 5th to 50th percentile
    # This allows the algorithm to find lower cutoffs if appropriate
    if xmin_range is None:
        # Set search range for xmin (as tuple of min, max)
        xmin_min = np.percentile(areas, 5)
        xmin_max = np.percentile(areas, 50)
        fit = powerlaw.Fit(areas, xmin=(xmin_min, xmin_max))
    else:
        fit = powerlaw.Fit(areas, xmin=(xmin_range[0], xmin_range[1]))
    
    # Get parameters
    cutoff = fit.power_law.xmin
    alpha = fit.power_law.alpha  # This is the exponent (positive)
    beta = -alpha  # Convert to negative as used in mLS
    
    # Estimate errors using bootstrap (if sigma is available)
    if hasattr(fit.power_law, 'sigma'):
        beta_error = fit.power_law.sigma
    else:
        # Fallback error estimation
        data = areas[areas >= cutoff]
        n = len(data)
        beta_error = abs(alpha - 1) / np.sqrt(n)
    
    # Estimate cutoff error (use ~10% as rough estimate)
    cutoff_error = cutoff * 0.1
    
    return cutoff, beta, cutoff_error, beta_error, 'official'


def estimate_powerlaw_parameters_simplified(areas, xmin_range=None):
    """
    Estimate power-law parameters using simplified KS-based method.
    
    This is a faster but less accurate implementation based on
    Clauset et al. (2009) principles.
    
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
        Estimated power-law exponent (negative)
    cutoff_error : float
        Estimated error in cutoff
    beta_error : float
        Estimated error in beta
    method : str
        Method used ('official' or 'simplified')
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
    
    return best_cutoff, best_beta, cutoff_error, beta_error, 'simplified'


def estimate_powerlaw_parameters(areas, xmin_range=None, method='auto'):
    """
    Estimate power-law parameters (cutoff and beta) for area distribution.
    
    Automatically uses the official powerlaw package if available,
    otherwise falls back to simplified method.
    
    Parameters:
    -----------
    areas : array-like
        Landslide areas in square meters
    xmin_range : tuple, optional
        (min, max) range for cutoff search
    method : str, optional
        'auto' (default): Use official if available, else simplified
        'official': Force use of official powerlaw package
        'simplified': Force use of simplified method
        
    Returns:
    --------
    cutoff : float
        Estimated cutoff value (xmin)
    beta : float
        Estimated power-law exponent (negative)
    cutoff_error : float
        Estimated error in cutoff
    beta_error : float
        Estimated error in beta
    method_used : str
        Method actually used ('official' or 'simplified')
    """
    
    if method == 'official' and not POWERLAW_AVAILABLE:
        raise ImportError(
            "Official powerlaw package not installed. "
            "Install it with: pip install powerlaw"
        )
    
    if method == 'simplified' or (method == 'auto' and not POWERLAW_AVAILABLE):
        return estimate_powerlaw_parameters_simplified(areas, xmin_range)
    else:
        return estimate_powerlaw_parameters_official(areas, xmin_range)


if __name__ == "__main__":
    # Test with synthetic data
    print("Power-law Parameter Estimator")
    print(f"Official powerlaw package available: {POWERLAW_AVAILABLE}")
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
    
    print(f"\nTest with synthetic data:")
    print(f"True values: cutoff={true_cutoff}, beta={true_beta}")
    
    # Test with auto method
    cutoff_est, beta_est, cutoff_err, beta_err, method = estimate_powerlaw_parameters(
        synthetic_areas, method='auto'
    )
    print(f"\nAuto method (using {method}):")
    print(f"  Cutoff: {cutoff_est:.2f} ± {cutoff_err:.2f}")
    print(f"  Beta: {beta_est:.2f} ± {beta_err:.2f}")
    
    # Test simplified method explicitly
    cutoff_est2, beta_est2, cutoff_err2, beta_err2, method2 = estimate_powerlaw_parameters(
        synthetic_areas, method='simplified'
    )
    print(f"\nSimplified method:")
    print(f"  Cutoff: {cutoff_est2:.2f} ± {cutoff_err2:.2f}")
    print(f"  Beta: {beta_est2:.2f} ± {beta_err2:.2f}")
