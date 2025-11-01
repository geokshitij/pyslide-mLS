% Test script to verify MATLAB mLS implementation
% Load all required data
load('sample_data.mat');
load('beta.mat');
load('beta_error.mat');
load('cutoff.mat');
load('cutoff_error.mat');

% Display input parameters
fprintf('\n========================================\n');
fprintf('MATLAB TEST - Input Parameters\n');
fprintf('========================================\n');
fprintf('Number of landslides: %d\n', length(Area));
fprintf('Total landslide area: %.2f m²\n', sum(Area));
fprintf('Min area: %.2f m²\n', min(Area));
fprintf('Max area: %.2f m²\n', max(Area));
fprintf('Mean area: %.2f m²\n', mean(Area));
fprintf('Median area: %.2f m²\n', median(Area));
fprintf('\n');
fprintf('Beta: %.4f\n', beta);
fprintf('Beta error: %.4f\n', beta_error);
fprintf('Cutoff: %.2f m²\n', cutoff);
fprintf('Cutoff error: %.2f m²\n', cutoff_error);

% Run mLS calculation
fprintf('\n========================================\n');
fprintf('Running MATLAB mLS calculation...\n');
fprintf('========================================\n');
[mLS_matlab, error_matlab] = mLS(Area, cutoff, beta, beta_error, cutoff_error);

% Display results
fprintf('\nMATLAB RESULTS:\n');
fprintf('mLS = %.4f\n', mLS_matlab);
fprintf('Uncertainty = ± %.4f\n', error_matlab);

fprintf('\n========================================\n');
fprintf('COMPARISON WITH PYTHON\n');
fprintf('========================================\n');
fprintf('Python mLS:        3.6273\n');
fprintf('Python uncertainty: ± 0.0846\n');
fprintf('\n');
fprintf('MATLAB mLS:        %.4f\n', mLS_matlab);
fprintf('MATLAB uncertainty: ± %.4f\n', error_matlab);
fprintf('\n');
fprintf('Difference in mLS: %.6f\n', abs(3.6273 - mLS_matlab));
fprintf('Difference in uncertainty: %.6f\n', abs(0.0846 - error_matlab));
fprintf('\n');

% Check if results match (within reasonable tolerance)
if abs(3.6273 - mLS_matlab) < 0.001 && abs(0.0846 - error_matlab) < 0.01
    fprintf('✓ RESULTS MATCH! Python and MATLAB implementations are consistent.\n');
else
    fprintf('⚠ RESULTS DIFFER! Please investigate the differences.\n');
end
fprintf('========================================\n\n');
