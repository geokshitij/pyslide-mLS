"""
Test script to verify the mLS calculator installation and functionality.
"""

import sys
import numpy as np

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing package imports...")
    
    try:
        import flask
        print(f"  ✅ Flask {flask.__version__}")
    except ImportError as e:
        print(f"  ❌ Flask import failed: {e}")
        return False
    
    try:
        import geopandas
        print(f"  ✅ GeoPandas {geopandas.__version__}")
    except ImportError as e:
        print(f"  ❌ GeoPandas import failed: {e}")
        return False
    
    try:
        import matplotlib
        print(f"  ✅ Matplotlib {matplotlib.__version__}")
    except ImportError as e:
        print(f"  ❌ Matplotlib import failed: {e}")
        return False
    
    try:
        import scipy
        print(f"  ✅ SciPy {scipy.__version__}")
    except ImportError as e:
        print(f"  ❌ SciPy import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"  ✅ NumPy {np.__version__}")
    except ImportError as e:
        print(f"  ❌ NumPy import failed: {e}")
        return False
    
    return True


def test_mls_calculator():
    """Test the mLS calculator with synthetic data."""
    print("\nTesting mLS calculator...")
    
    try:
        from mls_calculator import calculate_mls
        
        # Generate synthetic power-law distributed data
        np.random.seed(42)
        true_beta = -2.3
        true_cutoff = 100
        n_samples = 1000
        
        # Generate power-law distributed areas
        u = np.random.uniform(0, 1, n_samples)
        alpha = abs(true_beta) - 1
        synthetic_areas = true_cutoff * (1 - u) ** (-1/alpha)
        
        # Calculate mLS
        mls_value, error, plot_base64 = calculate_mls(
            synthetic_areas, 
            cutoff=true_cutoff, 
            beta=true_beta
        )
        
        print(f"  ✅ mLS calculation successful")
        print(f"     mLS value: {mls_value:.2f}")
        print(f"     Error: {error}")
        print(f"     Plot generated: {len(plot_base64) > 0}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ mLS calculator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_powerlaw_estimator():
    """Test the power-law parameter estimator."""
    print("\nTesting power-law parameter estimator...")
    
    try:
        from powerlaw_estimator import estimate_powerlaw_parameters
        
        # Generate synthetic power-law distributed data
        np.random.seed(42)
        true_beta = -2.3
        true_cutoff = 100
        n_samples = 1000
        
        u = np.random.uniform(0, 1, n_samples)
        alpha = abs(true_beta) - 1
        synthetic_areas = true_cutoff * (1 - u) ** (-1/alpha)
        
        # Estimate parameters
        cutoff_est, beta_est, cutoff_err, beta_err = estimate_powerlaw_parameters(synthetic_areas)
        
        print(f"  ✅ Parameter estimation successful")
        print(f"     Estimated cutoff: {cutoff_est:.2f} (true: {true_cutoff})")
        print(f"     Estimated beta: {beta_est:.2f} (true: {true_beta})")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Parameter estimator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("mLS Calculator - Installation Test")
    print("="*60)
    print()
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test mLS calculator
    if not test_mls_calculator():
        all_passed = False
    
    # Test parameter estimator
    if not test_powerlaw_estimator():
        all_passed = False
    
    print()
    print("="*60)
    if all_passed:
        print("✅ All tests passed! The application is ready to use.")
        print("\nTo start the application, run:")
        print("  python app.py")
        print("\nOr use the convenience script:")
        print("  ./run.sh")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nMake sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
