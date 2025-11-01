# 🏔️ pyslide-mLS# mLS



**Python implementation of the landslide-event magnitude scale (mLS) calculator with web interface**## Introduction



[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)mLS is a function that estimates the landslide magnitude (mLS) from cutoff 

[![License](https://img.shields.io/badge/license-Public%20Domain-green.svg)](LICENSE.md)(smallest area that follows power law), beta (power-law exponent), and an 

[![Flask](https://img.shields.io/badge/flask-3.0.0-lightgrey.svg)](https://flask.palletsprojects.com/)array of areas derived from a landslide inventory following the methods of 

Tanyas and others (2018). It can also calculate the uncertainty in 

---landslide-event magnitude if uncertainties in cutoff and beta values are 

given as input parameters. The function plots the best power-law fit for 

## 📖 Overviewthe medium and large landslides and the frequency-area distribution of the 

analyzed inventory. It also returns the corresponding mLS (landslide-event magnitude)

This repository provides both **MATLAB** and **Python** implementations for estimating landslide-event magnitude (mLS) from landslide inventory shapefiles. The Python version includes a user-friendly **Flask web interface** for easy analysis through your browser.value.



The methodology follows:To obtain the cutoff and beta values the method suggested by Clauset et al.(2009) 

> **Tanyas, H., K.E. Allstadt, and C.J. van Westen**, 2018. *An updated method for estimating landslide-event magnitude*. Earth Surface Processes and Landforms. DOI: [10.1002/esp.4359](https://doi.org/10.1002/esp.4359)can be used. The original scripts (plfit.m and plvar.m) of Clauset et al. (2009)

can be downloaded from the following link to calculate these parameters: 

### What is mLS?http://www.santafe.edu/~aaronc/powerlaws/ 



**mLS (landslide-event magnitude scale)** is analogous to earthquake magnitude scales but quantifies the overall size/severity of a landslide event. It's calculated from the frequency-area distribution of landslides following power-law statistics.### To install this function:



- **Input**: Landslide polygon areas from an inventoryDownload mLS.m and add it to your matlab path

- **Output**: 

  - mLS value (magnitude scale similar to earthquake scales)## Usage example (from mLS.m)

  - Power-law parameters (β exponent, cutoff point)

  - Uncertainty estimates```

  - Frequency-area distribution plot% Upload the landslide areas, which you want to analyze their frequency-area 

% distribution, as a horizontal array. In this example, we use the sample_data.m

---% file that you can find in the repository. When you open the sample_data.m

% file in the Matlab, you will see the landslide areas array with a parameter name

## ✨ Features% of 'Area'. This is the only input we need to run this code. In addition to that

% you can also use the uncertainty in the estimated power-law parameters to calculate

### Python Web Application% the uncertainty in mLS. To reach those uncertainty estimates you can open 

- 🌐 **Browser-based interface** - No coding required% the cutoff_error.m and beta_error.m files, and use them as an input of this function.

- 📁 **Shapefile upload** - Direct ZIP file support% Noted that this function can be run with or without considering the estimates of 

- 🔄 **Multiple shapefile handling** - Select from multiple shapefiles in one ZIP% uncertainties. 

- 📊 **Interactive results** - View plots and statistics in your browser

- 🎯 **Automatic parameter estimation** - Uses Clauset et al. (2009) method% In the following lines, the bins are defined with an array. We took 2 as 

- 📈 **Uncertainty quantification** - Monte Carlo simulation (10,000 iterations)% the minimum bin size and we used increasing bin sizes. We increase the 

- 🗺️ **Automatic CRS handling** - Converts to appropriate projected CRS for area calculation% bin widths while the landslide size increases, so that bin widths become

% approximately equal in logarithmic coordinates. To create a long array for 

### MATLAB Implementation% the bins we tentatively pick 120 for the size of x1 vector defined below.

- 🔬 **Original reference implementation** - For verification and academic usex1(1,1)=2;

- 📐 **Direct calculation** - Command-line interface for batch processingfor i=2:120

    x1(1,i)=x1(1,i-1)*1.2;

---end

x2=log10(x1);

## 🚀 Quick Start

Freq=histc(Area,x1); %Frequency values are calculated for each bin 

### Python Web Applications=size(x1);

s=s(1,2);

1. **Clone the repository**internal=zeros(1,s);

   ```bash

   git clone https://github.com/geokshitij/pyslide-mLS.gitfor i=2:s

   cd pyslide-mLS     internal(1,i)=x1(1,i)-x1(1,i-1);

   ```end

internal(1,1)=min(x1);

2. **Run the setup script**FD=Freq./internal;

   ```bash

   chmod +x run.shx1_rev = abs(x1-cutoff);    % the index of value that is closest to cutoff value is identified along the x1 array 

   ./run.sh[indexMidpoint indexMidpoint] = min(x1_rev);

   ```

x=x1(indexMidpoint:end); % the x (size bines) array for the frequeny-size distribution is defined 

3. **Open your browser**y=FD(indexMidpoint:end); % the y (frequency densities) array for the frequeny-size distribution is defined 

   - Navigate to: `http://localhost:5001`

   - Upload your landslide inventory shapefile (as ZIP)if beta>0           % beta value have to be negative

   - View results!    beta=-1*beta;

end

### Manual Installationbeta_stored=beta;



If the automatic script doesn't work:constant=y(1,1)/cutoff^beta;     % The c constant is calculated along the power-low where x=cutoff

fit_y=constant*x1.^beta;        % Frequency-density values calculated for the defined power-law fit

```bashfit_y_stored=fit_y;             

# Create virtual environment

python3 -m venv venvmidx=10^((log10(max(Area))+(log10(cutoff)))/2);     % The x and y values at mid-point location is read along the power-law fit

source venv/bin/activate  # On Windows: venv\Scripts\activatemidy=constant*midx^beta;



# Install dependenciesRefmidx=4.876599623713225e+04;    % X value for the mid point of the Northridge (reference point) inventory

pip install -r requirements.txtRefmidy=8.364725347860417e-04;    % Y value for the mid point of the Northridge (reference point) inventory

ac=Refmidy/(11111*Refmidx^beta);  % the c' constant (as) is calculated here for the mid-point of 

# Run the application                                  % the Northridge inventory as a reference point where mLS=log(11111) 

python app.py                             

```mLS=log10((midy/(ac*midx^(beta)))); % mLS is calculated in this line

mLS_stored=mLS;

---

% Uncertainty in mLS will be calculated if the required inputs are given

## 📂 Repository Structure% To do that Monte-Carlo simulation is run 10,000 times 



```if exist('beta_error')==1 && exist('cutoff_error')==1  

pyslide-mLS/    beta_interval_N=((beta+beta_error)-(beta-beta_error))/(499); %Number of elements to create an array including 500 uniformly distributed beta values is defined 

├── app.py                      # Flask web application    beta_interval=(beta-beta_error):beta_interval_N:(beta+beta_error);  %An array including 500 uniformly distributed beta values is defined     

├── mls_calculator.py           # Core mLS calculation module

├── powerlaw_estimator.py       # Automatic parameter estimation    cutoff_min=(cutoff-cutoff_error); 

├── requirements.txt            # Python dependencies        if cutoff_min<=0

├── run.sh                      # Setup and launch script             cutoff_min=2;

├── static/                     # CSS styles        else

├── templates/                  # HTML templates             cutoff_min=cutoff_min;

│   ├── index.html             # Upload page        end

│   ├── select_shapefile.html  # Multiple shapefile selection    cutoff_max=(cutoff+cutoff_error);

│   ├── results.html           # Results display    cutoff_interval_N=((cutoff_max)-(cutoff_min))/(499);    %Number of elements to create an array including 500 uniformly distributed cutoff values is defined 

│   └── about.html             # Documentation    cutoff_interval=(cutoff_min):cutoff_interval_N:(cutoff_max); %An array including 500 uniformly distributed cutoff values is defined   

├── matlab_original/           # Original MATLAB implementation

│   ├── mLS.m                  # MATLAB function    beta_mean=mean(beta_interval); %Mean of beta values is identified

│   ├── sample_data.mat        # Sample landslide areas    beta_std=std(beta_interval);    %Standard deviation of beta vaues is identified

│   ├── beta.mat               # Sample beta value    cutoff_mean=mean(cutoff_interval);  %Mean of cutoff values is identified

│   ├── beta_error.mat         # Sample beta uncertainty    cutoff_std=std(cutoff_interval);    %Standard deviation of cutoff values is identified

│   ├── cutoff.mat             # Sample cutoff value    

│   └── cutoff_error.mat       # Sample cutoff uncertainty        for i=1:10000   %mLS values are calculated for randomly sampled beta and cutoff values below

├── tests/                     # Test scripts and sample data            cutoff=normrnd(cutoff_mean,cutoff_std);

│   ├── test_matlab_comparison.py            beta=normrnd(beta_mean,beta_std);

│   ├── test_installation.py            constant=y(1,1)/cutoff^beta;

│   ├── generate_test_shapefile.py            fit_y=constant*x1.^beta; 

│   └── *.zip                  # Test shapefiles            midx=10^((log10(max(Area))+(log10(cutoff)))/2);

├── docs/                      # Additional documentation            ac=Refmidy/(11111*Refmidx^beta);

└── output/                    # Generated outputs            mLS_array(i,1)=log10((midy/(ac*midx^(beta))));

```        end



---    mLS_array=mLS_array(all(~isinf(mLS_array),2),:); % "Inf" cells are removed from the array  

    error=std(mLS_array(:));    %Uncertainty of mLS calcultated as a first standard deviation of mLS values

## 📊 Usageelse

    disp('Uncertainty in mLS will not be calculated because the variable "cutoff_error" and "beta_error" is missing')

### Web Interface    error='?'

end

1. **Upload Shapefile**

   - Prepare your landslide inventory as polygons in a shapefile% A graph showing the frequency-area distribution of the given landslides 

   - ZIP the shapefile (include .shp, .shx, .dbf, .prj files)% and the corresponding power-law fit are plotted.

   - Upload via the web interfaceloglog(x1,fit_y_stored,'-','LineWidth',2,'Color','r');hold on

loglog(x1,FD,'ok','MarkerSize',8,'MarkerFaceColor','b','MarkerEdgeColor','k')

2. **Select Shapefile** (if multiple in ZIP)axis([1 1.E+7 1.E-6 1000])

   - Choose which shapefile to analyzeset(get(gca,'Xlabel'),'string','Landslide Area (m^2)','FontSize',12, 'FontUnits','points','FontWeight','normal')

   - Optionally provide known beta/cutoff values or let the system estimate themset(get(gca,'Ylabel'),'string','Frequency Density (m^-^2)','FontSize',12, 'FontUnits','points','FontWeight','normal')

str={['\beta = ',num2str(beta_stored)];['mLS = ',num2str(mLS_stored),(char(177)),num2str(error)]};

3. **View Results**text(x1(1,1),(min(FD(FD>0)*10)),str,'FontSize',12) 

   - mLS value with uncertainty

   - Power-law parameters (β, cutoff)% For the given sample data, the corresponding beta (power-law exponent), 

   - Frequency-area distribution plot% and mLS (landslide magnitude) values should be appeared as 

   - Inventory statistics% -2.46, and 3.63±0.08 respectively. A plot showing the frequency-area distribution 

% of the given landslides and the corresponding power-law fit is also output, see image below.

### Python Module```



```python![img1](sample_data_output.png)

from mls_calculator import calculate_mls

import geopandas as gpd## References



# Read shapefileClauset, A., Shalizi, C.R. and Newman, M.E., 2009. Power-law distributions in empirical data. SIAM review, 51(4): 661-703. DOI:10.1137/070710111

gdf = gpd.read_file('landslides.shp')

areas = gdf.geometry.area.valuesGuzzetti, F., Malamud, B.D., Turcotte, D.L. and Reichenbach, P., 2002. Power-law correlations of landslide areas in central Italy. Earth and Planetary Science Letters, 195(3): 169-183. DOI:10.1016/S0012-821X(01)00589-1



# Calculate mLS (with automatic parameter estimation)Stark, C.P. and Guzzetti, F., 2009. Landslide rupture and the probability distribution of mobilized debris volumes. Journal of Geophysical Research: Earth Surface, 114(F2). DOI:10.1029/2008JF001008

from powerlaw_estimator import estimate_powerlaw_parameters

Tanyas, H., Allstadt, K.E., and van Westen, C.J. (in press). An updated method for estimating landslide-event magnitude. Earth Surface Processes and Landforms.

beta, beta_error, cutoff, cutoff_error = estimate_powerlaw_parameters(areas)

mls, uncertainty, plot = calculate_mls(areas, beta, cutoff, beta_error, cutoff_error)Van Den Eeckhaut, M., Poesen, J., Govers, G., Verstraeten, G. and Demoulin, A., 2007. Characteristics of the size distribution of recent and historical landslides in a populated hilly region. Earth and Planetary Science Letters, 256(3): 588-603. DOI:10.1016/j.epsl.2007.01.040


print(f"mLS = {mls:.2f} ± {uncertainty:.2f}")
```

### MATLAB

```matlab
% Load data
load('matlab_original/sample_data.mat');
load('matlab_original/beta.mat');
load('matlab_original/cutoff.mat');
load('matlab_original/beta_error.mat');
load('matlab_original/cutoff_error.mat');

% Calculate mLS
[mLS_value, error] = mLS(Area, cutoff, beta, beta_error, cutoff_error);

fprintf('mLS = %.2f ± %.2f\n', mLS_value, error);
```

---

## 🧪 Verification

To verify that Python and MATLAB implementations produce identical results:

```bash
# Run Python test
python tests/test_matlab_comparison.py

# Run MATLAB test
matlab -r "cd tests; test_matlab; exit"
```

Expected output (using sample data):
- **mLS**: 3.6273
- **Uncertainty**: ± 0.0846

---

## 📋 Requirements

### Python
- Python 3.9 or higher
- Flask 3.0.0
- GeoPandas 1.1.1
- NumPy 2.3.4
- Matplotlib 3.10.7
- SciPy 1.16.3
- See `requirements.txt` for complete list

### MATLAB
- MATLAB R2015b or higher
- No additional toolboxes required

---

## 📐 Methodology

The mLS calculation follows these steps:

1. **Load landslide areas** from shapefile polygons
2. **Estimate power-law parameters** using Clauset et al. (2009) method:
   - **Cutoff (xmin)**: Minimum area where power-law behavior begins
   - **Beta (β)**: Power-law exponent (slope)
3. **Calculate frequency-area distribution** using logarithmic bins
4. **Fit power-law** to medium/large landslides (above cutoff)
5. **Compute mLS** using reference inventory (1994 Northridge)
6. **Quantify uncertainty** via Monte Carlo simulation (10,000 iterations)

### Power-Law Distribution

The frequency-area distribution follows:

$$p(A) = c \cdot A^{\beta}$$

where:
- $A$ = landslide area (m²)
- $\beta$ = power-law exponent (typically -1.4 to -3.4)
- $c$ = normalization constant

### mLS Formula

$$mLS = \log_{10}\left(\frac{p(A_{mid})}{c' \cdot A_{mid}^{\beta}}\right)$$

where $A_{mid}$ is the geometric mean of cutoff and maximum area.

---

## 🎯 Interpretation

### mLS Scale
- **< 2.0**: Small event (e.g., Loma Prieta 1989, mLS = 1.75)
- **2.0 - 3.5**: Moderate event (e.g., Yushu 2010, mLS = 2.76)
- **3.5 - 5.0**: Large event (e.g., Kashmir 2005, mLS = 4.85)
- **> 5.0**: Major/catastrophic event (e.g., Wenchuan 2008, mLS = 6.15)

### Beta (β) Values
- **-1.5 to -2.0**: Relatively more large landslides
- **-2.3 to -2.5**: Typical range (central tendency)
- **-3.0 to -3.5**: Dominated by smaller landslides

### Cutoff Point
- Indicates **inventory completeness threshold**
- Below cutoff: mapping limitations, undersampling
- Above cutoff: reliable power-law region used for mLS

---

## 📚 References

**Primary Reference:**
- Tanyas, H., Allstadt, K.E., and van Westen, C.J., 2018. An updated method for estimating landslide-event magnitude. *Earth Surface Processes and Landforms*, 43(9), 1836-1847. DOI: [10.1002/esp.4359](https://doi.org/10.1002/esp.4359)

**Supporting Literature:**
- Clauset, A., Shalizi, C.R., and Newman, M.E., 2009. Power-law distributions in empirical data. *SIAM Review*, 51(4), 661-703. DOI: [10.1137/070710111](https://doi.org/10.1137/070710111)
- Malamud, B.D., Turcotte, D.L., Guzzetti, F., and Reichenbach, P., 2004. Landslide inventories and their statistical properties. *Earth Surface Processes and Landforms*, 29(6), 687-711.
- Stark, C.P. and Guzzetti, F., 2009. Landslide rupture and the probability distribution of mobilized debris volumes. *Journal of Geophysical Research: Earth Surface*, 114(F2). DOI: [10.1029/2008JF001008](https://doi.org/10.1029/2008JF001008)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This software is released into the **public domain** for research and educational purposes. See [LICENSE.md](LICENSE.md) and [DISCLAIMER.md](DISCLAIMER.md) for details.

---

## 🙏 Acknowledgments

- Original MATLAB implementation by Hakan Tanyaş, Kate E. Allstadt, and Cees J. van Westen
- Python conversion and web interface development
- USGS Landslide Hazards Program

---

## 📧 Contact

For questions, issues, or suggestions:
- **GitHub Issues**: [github.com/geokshitij/pyslide-mLS/issues](https://github.com/geokshitij/pyslide-mLS/issues)
- **Citation**: If you use this tool in your research, please cite the Tanyas et al. (2018) paper

---

## 🔄 Version History

- **v1.0.0** (2025) - Initial Python implementation with web interface
  - Flask web application
  - Automatic parameter estimation
  - Multiple shapefile support
  - Improved visualization (power-law fit only in valid region)
  - Comprehensive testing and verification

---

**Made with ❤️ for the landslide research community**
