# 🏔️ pyslide-mLS# 🏔️ pyslide-mLS# mLS



**Python implementation of the landslide-event magnitude scale (mLS) calculator with web interface**



[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)**Python implementation of the landslide-event magnitude scale (mLS) calculator with web interface**## Introduction

[![License](https://img.shields.io/badge/license-Public%20Domain-green.svg)](LICENSE.md)

[![Flask](https://img.shields.io/badge/flask-3.0.0-lightgrey.svg)](https://flask.palletsprojects.com/)



---[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)mLS is a function that estimates the landslide magnitude (mLS) from cutoff 



## 📖 Overview[![License](https://img.shields.io/badge/license-Public%20Domain-green.svg)](LICENSE.md)(smallest area that follows power law), beta (power-law exponent), and an 



This repository provides both **MATLAB** and **Python** implementations for estimating landslide-event magnitude (mLS) from landslide inventory shapefiles. The Python version includes a user-friendly **Flask web interface** for easy analysis through your browser.[![Flask](https://img.shields.io/badge/flask-3.0.0-lightgrey.svg)](https://flask.palletsprojects.com/)array of areas derived from a landslide inventory following the methods of 



The methodology follows:Tanyas and others (2018). It can also calculate the uncertainty in 

> **Tanyas, H., K.E. Allstadt, and C.J. van Westen**, 2018. *An updated method for estimating landslide-event magnitude*. Earth Surface Processes and Landforms. DOI: [10.1002/esp.4359](https://doi.org/10.1002/esp.4359)

---landslide-event magnitude if uncertainties in cutoff and beta values are 

### What is mLS?

given as input parameters. The function plots the best power-law fit for 

**mLS (landslide-event magnitude scale)** is analogous to earthquake magnitude scales but quantifies the overall size/severity of a landslide event. It's calculated from the frequency-area distribution of landslides following power-law statistics.

## 📖 Overviewthe medium and large landslides and the frequency-area distribution of the 

- **Input**: Landslide polygon areas from an inventory

- **Output**: analyzed inventory. It also returns the corresponding mLS (landslide-event magnitude)

  - mLS value (magnitude scale similar to earthquake scales)

  - Power-law parameters (β exponent, cutoff point)This repository provides both **MATLAB** and **Python** implementations for estimating landslide-event magnitude (mLS) from landslide inventory shapefiles. The Python version includes a user-friendly **Flask web interface** for easy analysis through your browser.value.

  - Uncertainty estimates

  - Frequency-area distribution plot



---The methodology follows:To obtain the cutoff and beta values the method suggested by Clauset et al.(2009) 



## ✨ Features> **Tanyas, H., K.E. Allstadt, and C.J. van Westen**, 2018. *An updated method for estimating landslide-event magnitude*. Earth Surface Processes and Landforms. DOI: [10.1002/esp.4359](https://doi.org/10.1002/esp.4359)can be used. The original scripts (plfit.m and plvar.m) of Clauset et al. (2009)



### Python Web Applicationcan be downloaded from the following link to calculate these parameters: 

- 🌐 **Browser-based interface** - No coding required

- 📁 **Shapefile upload** - Direct ZIP file support### What is mLS?http://www.santafe.edu/~aaronc/powerlaws/ 

- 🔄 **Multiple shapefile handling** - Select from multiple shapefiles in one ZIP

- 📊 **Interactive results** - View plots and statistics in your browser

- 🎯 **Automatic parameter estimation** - Uses Clauset et al. (2009) method

- 📈 **Uncertainty quantification** - Monte Carlo simulation (10,000 iterations)**mLS (landslide-event magnitude scale)** is analogous to earthquake magnitude scales but quantifies the overall size/severity of a landslide event. It's calculated from the frequency-area distribution of landslides following power-law statistics.### To install this function:

- 🗺️ **Automatic CRS handling** - Converts to appropriate projected CRS for area calculation



### MATLAB Implementation

- 🔬 **Original reference implementation** - For verification and academic use- **Input**: Landslide polygon areas from an inventoryDownload mLS.m and add it to your matlab path

- 📐 **Direct calculation** - Command-line interface for batch processing

- **Output**: 

---

  - mLS value (magnitude scale similar to earthquake scales)## Usage example (from mLS.m)

## 🚀 Quick Start

  - Power-law parameters (β exponent, cutoff point)

### Python Web Application

  - Uncertainty estimates```

1. **Clone the repository**

   ```bash  - Frequency-area distribution plot% Upload the landslide areas, which you want to analyze their frequency-area 

   git clone https://github.com/geokshitij/pyslide-mLS.git

   cd pyslide-mLS% distribution, as a horizontal array. In this example, we use the sample_data.m

   ```

---% file that you can find in the repository. When you open the sample_data.m

2. **Run the setup script**

   ```bash% file in the Matlab, you will see the landslide areas array with a parameter name

   chmod +x run.sh

   ./run.sh## ✨ Features% of 'Area'. This is the only input we need to run this code. In addition to that

   ```

% you can also use the uncertainty in the estimated power-law parameters to calculate

3. **Open your browser**

   - Navigate to: `http://localhost:5001`### Python Web Application% the uncertainty in mLS. To reach those uncertainty estimates you can open 

   - Upload your landslide inventory shapefile (as ZIP)

   - View results!- 🌐 **Browser-based interface** - No coding required% the cutoff_error.m and beta_error.m files, and use them as an input of this function.



### Manual Installation- 📁 **Shapefile upload** - Direct ZIP file support% Noted that this function can be run with or without considering the estimates of 



If the automatic script doesn't work:- 🔄 **Multiple shapefile handling** - Select from multiple shapefiles in one ZIP% uncertainties. 



```bash- 📊 **Interactive results** - View plots and statistics in your browser

# Create virtual environment

python3 -m venv venv- 🎯 **Automatic parameter estimation** - Uses Clauset et al. (2009) method% In the following lines, the bins are defined with an array. We took 2 as 

source venv/bin/activate  # On Windows: venv\Scripts\activate

- 📈 **Uncertainty quantification** - Monte Carlo simulation (10,000 iterations)% the minimum bin size and we used increasing bin sizes. We increase the 

# Install dependencies

pip install -r requirements.txt- 🗺️ **Automatic CRS handling** - Converts to appropriate projected CRS for area calculation% bin widths while the landslide size increases, so that bin widths become



# Run the application% approximately equal in logarithmic coordinates. To create a long array for 

python app.py

```### MATLAB Implementation% the bins we tentatively pick 120 for the size of x1 vector defined below.



---- 🔬 **Original reference implementation** - For verification and academic usex1(1,1)=2;



## 📂 Repository Structure- 📐 **Direct calculation** - Command-line interface for batch processingfor i=2:120



```    x1(1,i)=x1(1,i-1)*1.2;

pyslide-mLS/

├── app.py                      # Flask web application---end

├── mls_calculator.py           # Core mLS calculation module

├── powerlaw_estimator.py       # Automatic parameter estimationx2=log10(x1);

├── requirements.txt            # Python dependencies

├── run.sh                      # Setup and launch script## 🚀 Quick Start

├── static/                     # CSS styles

├── templates/                  # HTML templatesFreq=histc(Area,x1); %Frequency values are calculated for each bin 

│   ├── index.html             # Upload page

│   ├── select_shapefile.html  # Multiple shapefile selection### Python Web Applications=size(x1);

│   ├── results.html           # Results display

│   └── about.html             # Documentations=s(1,2);

├── matlab_original/           # Original MATLAB implementation

│   ├── mLS.m                  # MATLAB function1. **Clone the repository**internal=zeros(1,s);

│   ├── sample_data.mat        # Sample landslide areas

│   ├── beta.mat               # Sample beta value   ```bash

│   ├── beta_error.mat         # Sample beta uncertainty

│   ├── cutoff.mat             # Sample cutoff value   git clone https://github.com/geokshitij/pyslide-mLS.gitfor i=2:s

│   └── cutoff_error.mat       # Sample cutoff uncertainty

├── tests/                     # Test scripts and sample data   cd pyslide-mLS     internal(1,i)=x1(1,i)-x1(1,i-1);

│   ├── test_matlab_comparison.py

│   ├── test_installation.py   ```end

│   ├── generate_test_shapefile.py

│   └── *.zip                  # Test shapefilesinternal(1,1)=min(x1);

├── docs/                      # Additional documentation

└── output/                    # Generated outputs2. **Run the setup script**FD=Freq./internal;

```

   ```bash

---

   chmod +x run.shx1_rev = abs(x1-cutoff);    % the index of value that is closest to cutoff value is identified along the x1 array 

## 📊 Usage

   ./run.sh[indexMidpoint indexMidpoint] = min(x1_rev);

### Web Interface

   ```

1. **Upload Shapefile**

   - Prepare your landslide inventory as polygons in a shapefilex=x1(indexMidpoint:end); % the x (size bines) array for the frequeny-size distribution is defined 

   - ZIP the shapefile (include .shp, .shx, .dbf, .prj files)

   - Upload via the web interface3. **Open your browser**y=FD(indexMidpoint:end); % the y (frequency densities) array for the frequeny-size distribution is defined 



2. **Select Shapefile** (if multiple in ZIP)   - Navigate to: `http://localhost:5001`

   - Choose which shapefile to analyze

   - Optionally provide known beta/cutoff values or let the system estimate them   - Upload your landslide inventory shapefile (as ZIP)if beta>0           % beta value have to be negative



3. **View Results**   - View results!    beta=-1*beta;

   - mLS value with uncertainty

   - Power-law parameters (β, cutoff)end

   - Frequency-area distribution plot

   - Inventory statistics### Manual Installationbeta_stored=beta;



### Python Module



```pythonIf the automatic script doesn't work:constant=y(1,1)/cutoff^beta;     % The c constant is calculated along the power-low where x=cutoff

from mls_calculator import calculate_mls

import geopandas as gpdfit_y=constant*x1.^beta;        % Frequency-density values calculated for the defined power-law fit



# Read shapefile```bashfit_y_stored=fit_y;             

gdf = gpd.read_file('landslides.shp')

areas = gdf.geometry.area.values# Create virtual environment



# Calculate mLS (with automatic parameter estimation)python3 -m venv venvmidx=10^((log10(max(Area))+(log10(cutoff)))/2);     % The x and y values at mid-point location is read along the power-law fit

from powerlaw_estimator import estimate_powerlaw_parameters

source venv/bin/activate  # On Windows: venv\Scripts\activatemidy=constant*midx^beta;

beta, beta_error, cutoff, cutoff_error = estimate_powerlaw_parameters(areas)

mls, uncertainty, plot = calculate_mls(areas, beta, cutoff, beta_error, cutoff_error)



print(f"mLS = {mls:.2f} ± {uncertainty:.2f}")# Install dependenciesRefmidx=4.876599623713225e+04;    % X value for the mid point of the Northridge (reference point) inventory

```

pip install -r requirements.txtRefmidy=8.364725347860417e-04;    % Y value for the mid point of the Northridge (reference point) inventory

### MATLAB

ac=Refmidy/(11111*Refmidx^beta);  % the c' constant (as) is calculated here for the mid-point of 

```matlab

% Load data# Run the application                                  % the Northridge inventory as a reference point where mLS=log(11111) 

load('matlab_original/sample_data.mat');

load('matlab_original/beta.mat');python app.py                             

load('matlab_original/cutoff.mat');

load('matlab_original/beta_error.mat');```mLS=log10((midy/(ac*midx^(beta)))); % mLS is calculated in this line

load('matlab_original/cutoff_error.mat');

mLS_stored=mLS;

% Calculate mLS

[mLS_value, error] = mLS(Area, cutoff, beta, beta_error, cutoff_error);---



fprintf('mLS = %.2f ± %.2f\n', mLS_value, error);% Uncertainty in mLS will be calculated if the required inputs are given

```

## 📂 Repository Structure% To do that Monte-Carlo simulation is run 10,000 times 

---



## 🧪 Verification

```if exist('beta_error')==1 && exist('cutoff_error')==1  

To verify that Python and MATLAB implementations produce identical results:

pyslide-mLS/    beta_interval_N=((beta+beta_error)-(beta-beta_error))/(499); %Number of elements to create an array including 500 uniformly distributed beta values is defined 

```bash

# Run Python test├── app.py                      # Flask web application    beta_interval=(beta-beta_error):beta_interval_N:(beta+beta_error);  %An array including 500 uniformly distributed beta values is defined     

python tests/test_matlab_comparison.py

├── mls_calculator.py           # Core mLS calculation module

# Run MATLAB test (if you have MATLAB installed)

matlab -r "cd tests; test_matlab; exit"├── powerlaw_estimator.py       # Automatic parameter estimation    cutoff_min=(cutoff-cutoff_error); 

```

├── requirements.txt            # Python dependencies        if cutoff_min<=0

Expected output (using sample data):

- **mLS**: 3.6273├── run.sh                      # Setup and launch script             cutoff_min=2;

- **Uncertainty**: ± 0.0846

├── static/                     # CSS styles        else

---

├── templates/                  # HTML templates             cutoff_min=cutoff_min;

## 📋 Requirements

│   ├── index.html             # Upload page        end

### Python

- Python 3.9 or higher│   ├── select_shapefile.html  # Multiple shapefile selection    cutoff_max=(cutoff+cutoff_error);

- Flask 3.0.0

- GeoPandas 1.1.1│   ├── results.html           # Results display    cutoff_interval_N=((cutoff_max)-(cutoff_min))/(499);    %Number of elements to create an array including 500 uniformly distributed cutoff values is defined 

- NumPy 2.3.4

- Matplotlib 3.10.7│   └── about.html             # Documentation    cutoff_interval=(cutoff_min):cutoff_interval_N:(cutoff_max); %An array including 500 uniformly distributed cutoff values is defined   

- SciPy 1.16.3

- See `requirements.txt` for complete list├── matlab_original/           # Original MATLAB implementation



### MATLAB│   ├── mLS.m                  # MATLAB function    beta_mean=mean(beta_interval); %Mean of beta values is identified

- MATLAB R2015b or higher

- No additional toolboxes required│   ├── sample_data.mat        # Sample landslide areas    beta_std=std(beta_interval);    %Standard deviation of beta vaues is identified



---│   ├── beta.mat               # Sample beta value    cutoff_mean=mean(cutoff_interval);  %Mean of cutoff values is identified



## 📐 Methodology│   ├── beta_error.mat         # Sample beta uncertainty    cutoff_std=std(cutoff_interval);    %Standard deviation of cutoff values is identified



The mLS calculation follows these steps:│   ├── cutoff.mat             # Sample cutoff value    



1. **Load landslide areas** from shapefile polygons│   └── cutoff_error.mat       # Sample cutoff uncertainty        for i=1:10000   %mLS values are calculated for randomly sampled beta and cutoff values below

2. **Estimate power-law parameters** using Clauset et al. (2009) method:

   - **Cutoff (xmin)**: Minimum area where power-law behavior begins├── tests/                     # Test scripts and sample data            cutoff=normrnd(cutoff_mean,cutoff_std);

   - **Beta (β)**: Power-law exponent (slope)

3. **Calculate frequency-area distribution** using logarithmic bins│   ├── test_matlab_comparison.py            beta=normrnd(beta_mean,beta_std);

4. **Fit power-law** to medium/large landslides (above cutoff)

5. **Compute mLS** using reference inventory (1994 Northridge)│   ├── test_installation.py            constant=y(1,1)/cutoff^beta;

6. **Quantify uncertainty** via Monte Carlo simulation (10,000 iterations)

│   ├── generate_test_shapefile.py            fit_y=constant*x1.^beta; 

### Power-Law Distribution

│   └── *.zip                  # Test shapefiles            midx=10^((log10(max(Area))+(log10(cutoff)))/2);

The frequency-area distribution follows:

├── docs/                      # Additional documentation            ac=Refmidy/(11111*Refmidx^beta);

$$p(A) = c \cdot A^{\beta}$$

└── output/                    # Generated outputs            mLS_array(i,1)=log10((midy/(ac*midx^(beta))));

where:

- $A$ = landslide area (m²)```        end

- $\beta$ = power-law exponent (typically -1.4 to -3.4)

- $c$ = normalization constant



### mLS Formula---    mLS_array=mLS_array(all(~isinf(mLS_array),2),:); % "Inf" cells are removed from the array  



$$mLS = \log_{10}\left(\frac{p(A_{mid})}{c' \cdot A_{mid}^{\beta}}\right)$$    error=std(mLS_array(:));    %Uncertainty of mLS calcultated as a first standard deviation of mLS values



where $A_{mid}$ is the geometric mean of cutoff and maximum area.## 📊 Usageelse



---    disp('Uncertainty in mLS will not be calculated because the variable "cutoff_error" and "beta_error" is missing')



## 🎯 Interpretation### Web Interface    error='?'



### mLS Scaleend

- **< 2.0**: Small event (e.g., Loma Prieta 1989, mLS = 1.75)

- **2.0 - 3.5**: Moderate event (e.g., Yushu 2010, mLS = 2.76)1. **Upload Shapefile**

- **3.5 - 5.0**: Large event (e.g., Kashmir 2005, mLS = 4.85)

- **> 5.0**: Major/catastrophic event (e.g., Wenchuan 2008, mLS = 6.15)   - Prepare your landslide inventory as polygons in a shapefile% A graph showing the frequency-area distribution of the given landslides 



### Beta (β) Values   - ZIP the shapefile (include .shp, .shx, .dbf, .prj files)% and the corresponding power-law fit are plotted.

- **-1.5 to -2.0**: Relatively more large landslides

- **-2.3 to -2.5**: Typical range (central tendency)   - Upload via the web interfaceloglog(x1,fit_y_stored,'-','LineWidth',2,'Color','r');hold on

- **-3.0 to -3.5**: Dominated by smaller landslides

loglog(x1,FD,'ok','MarkerSize',8,'MarkerFaceColor','b','MarkerEdgeColor','k')

### Cutoff Point

- Indicates **inventory completeness threshold**2. **Select Shapefile** (if multiple in ZIP)axis([1 1.E+7 1.E-6 1000])

- Below cutoff: mapping limitations, undersampling

- Above cutoff: reliable power-law region used for mLS   - Choose which shapefile to analyzeset(get(gca,'Xlabel'),'string','Landslide Area (m^2)','FontSize',12, 'FontUnits','points','FontWeight','normal')



---   - Optionally provide known beta/cutoff values or let the system estimate themset(get(gca,'Ylabel'),'string','Frequency Density (m^-^2)','FontSize',12, 'FontUnits','points','FontWeight','normal')



## 📚 Referencesstr={['\beta = ',num2str(beta_stored)];['mLS = ',num2str(mLS_stored),(char(177)),num2str(error)]};



**Primary Reference:**3. **View Results**text(x1(1,1),(min(FD(FD>0)*10)),str,'FontSize',12) 

- Tanyas, H., Allstadt, K.E., and van Westen, C.J., 2018. An updated method for estimating landslide-event magnitude. *Earth Surface Processes and Landforms*, 43(9), 1836-1847. DOI: [10.1002/esp.4359](https://doi.org/10.1002/esp.4359)

   - mLS value with uncertainty

**Supporting Literature:**

- Clauset, A., Shalizi, C.R., and Newman, M.E., 2009. Power-law distributions in empirical data. *SIAM Review*, 51(4), 661-703. DOI: [10.1137/070710111](https://doi.org/10.1137/070710111)   - Power-law parameters (β, cutoff)% For the given sample data, the corresponding beta (power-law exponent), 

- Malamud, B.D., Turcotte, D.L., Guzzetti, F., and Reichenbach, P., 2004. Landslide inventories and their statistical properties. *Earth Surface Processes and Landforms*, 29(6), 687-711.

- Stark, C.P. and Guzzetti, F., 2009. Landslide rupture and the probability distribution of mobilized debris volumes. *Journal of Geophysical Research: Earth Surface*, 114(F2). DOI: [10.1029/2008JF001008](https://doi.org/10.1029/2008JF001008)   - Frequency-area distribution plot% and mLS (landslide magnitude) values should be appeared as 



---   - Inventory statistics% -2.46, and 3.63±0.08 respectively. A plot showing the frequency-area distribution 



## 🤝 Contributing% of the given landslides and the corresponding power-law fit is also output, see image below.



Contributions are welcome! Please feel free to submit a Pull Request.### Python Module```



1. Fork the repository

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)```python![img1](sample_data_output.png)

4. Push to the branch (`git push origin feature/AmazingFeature`)

5. Open a Pull Requestfrom mls_calculator import calculate_mls



See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.import geopandas as gpd## References



---



## 📄 License# Read shapefileClauset, A., Shalizi, C.R. and Newman, M.E., 2009. Power-law distributions in empirical data. SIAM review, 51(4): 661-703. DOI:10.1137/070710111



This software is released into the **public domain** for research and educational purposes. See [LICENSE.md](LICENSE.md) and [DISCLAIMER.md](DISCLAIMER.md) for details.gdf = gpd.read_file('landslides.shp')



---areas = gdf.geometry.area.valuesGuzzetti, F., Malamud, B.D., Turcotte, D.L. and Reichenbach, P., 2002. Power-law correlations of landslide areas in central Italy. Earth and Planetary Science Letters, 195(3): 169-183. DOI:10.1016/S0012-821X(01)00589-1



## 🙏 Acknowledgments



- Original MATLAB implementation by Hakan Tanyaş, Kate E. Allstadt, and Cees J. van Westen# Calculate mLS (with automatic parameter estimation)Stark, C.P. and Guzzetti, F., 2009. Landslide rupture and the probability distribution of mobilized debris volumes. Journal of Geophysical Research: Earth Surface, 114(F2). DOI:10.1029/2008JF001008

- Python conversion and web interface development

- USGS Landslide Hazards Programfrom powerlaw_estimator import estimate_powerlaw_parameters



---Tanyas, H., Allstadt, K.E., and van Westen, C.J. (in press). An updated method for estimating landslide-event magnitude. Earth Surface Processes and Landforms.



## 📧 Contactbeta, beta_error, cutoff, cutoff_error = estimate_powerlaw_parameters(areas)



For questions, issues, or suggestions:mls, uncertainty, plot = calculate_mls(areas, beta, cutoff, beta_error, cutoff_error)Van Den Eeckhaut, M., Poesen, J., Govers, G., Verstraeten, G. and Demoulin, A., 2007. Characteristics of the size distribution of recent and historical landslides in a populated hilly region. Earth and Planetary Science Letters, 256(3): 588-603. DOI:10.1016/j.epsl.2007.01.040

- **GitHub Issues**: [github.com/geokshitij/pyslide-mLS/issues](https://github.com/geokshitij/pyslide-mLS/issues)

- **Citation**: If you use this tool in your research, please cite the Tanyas et al. (2018) paper

print(f"mLS = {mls:.2f} ± {uncertainty:.2f}")

---```



## 🔄 Version History### MATLAB



- **v1.0.0** (2025) - Initial Python implementation with web interface```matlab

  - Flask web application% Load data

  - Automatic parameter estimationload('matlab_original/sample_data.mat');

  - Multiple shapefile supportload('matlab_original/beta.mat');

  - Improved visualization (power-law fit only in valid region)load('matlab_original/cutoff.mat');

  - Comprehensive testing and verificationload('matlab_original/beta_error.mat');

load('matlab_original/cutoff_error.mat');

---

% Calculate mLS

**Made with ❤️ for the landslide research community**[mLS_value, error] = mLS(Area, cutoff, beta, beta_error, cutoff_error);


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
