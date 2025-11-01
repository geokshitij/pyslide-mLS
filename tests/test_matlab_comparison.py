"""
Test script to verify Python implementation matches MATLAB mLS.m results
"""
import scipy.io as sio
import numpy as np
from mls_calculator import calculate_mls

# Load the MATLAB sample data
print("Loading MATLAB sample data files...")
sample_data = sio.loadmat('sample_data.mat')
beta_data = sio.loadmat('beta.mat')
beta_error_data = sio.loadmat('beta_error.mat')
cutoff_data = sio.loadmat('cutoff.mat')
cutoff_error_data = sio.loadmat('cutoff_error.mat')

# Extract the values
Area = sample_data['Area'].flatten()
beta = float(beta_data['beta'])
beta_error = float(beta_error_data['beta_error'])
cutoff = float(cutoff_data['cutoff'])
cutoff_error = float(cutoff_error_data['cutoff_error'])

print("\n" + "="*60)
print("MATLAB INPUT PARAMETERS")
print("="*60)
print(f"Number of landslides: {len(Area)}")
print(f"Total landslide area: {np.sum(Area):.2f} m²")
print(f"Min area: {np.min(Area):.2f} m²")
print(f"Max area: {np.max(Area):.2f} m²")
print(f"Mean area: {np.mean(Area):.2f} m²")
print(f"Median area: {np.median(Area):.2f} m²")
print(f"\nBeta: {beta:.4f}")
print(f"Beta error: {beta_error:.4f}")
print(f"Cutoff: {cutoff:.2f} m²")
print(f"Cutoff error: {cutoff_error:.2f} m²")

# Run Python implementation
print("\n" + "="*60)
print("RUNNING PYTHON IMPLEMENTATION")
print("="*60)

mls_python, uncertainty_python, plot_base64 = calculate_mls(
    area=Area,
    beta=beta,
    cutoff=cutoff,
    beta_error=beta_error,
    cutoff_error=cutoff_error
)

print(f"\nmLS = {mls_python:.4f}")
print(f"Uncertainty = ± {uncertainty_python:.4f}")

# Expected MATLAB results (you should run the MATLAB code to get these)
print("\n" + "="*60)
print("COMPARISON WITH MATLAB")
print("="*60)
print("Run the MATLAB code with these exact inputs:")
print(">> load('sample_data.mat')")
print(">> load('beta.mat')")
print(">> load('beta_error.mat')")
print(">> load('cutoff.mat')")
print(">> load('cutoff_error.mat')")
print(">> [mLS_matlab, error_matlab] = mLS(Area, cutoff, beta, beta_error, cutoff_error)")
print("\nThen compare:")
print(f"Python mLS:        {mls_python:.4f}")
print(f"Python uncertainty: ± {uncertainty_python:.4f}")
print("\nWith MATLAB output...")

# Show detailed calculation steps for verification
print("\n" + "="*60)
print("DETAILED CALCULATION STEPS (for verification)")
print("="*60)
print(f"Reference point (Northridge):")
print(f"  Refmidx = 4.876599623713225e+04")
print(f"  Refmidy = 8.364725347860417e-04")
print(f"  N_ref = 11111")
print(f"\nYour data midpoint:")
print(f"  midx = 10^((log10({np.max(Area):.2f}) + log10({cutoff:.2f}))/2)")
print(f"  midx = {10**((np.log10(np.max(Area)) + np.log10(cutoff))/2):.6e}")
