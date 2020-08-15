# Who's Left Riding Transit During COVID-19? A Joint Modeling Using Bayesian Structural Time-Series and Partial Least Squares Regression
### Songhua Hu, Peng Chen 

## Data
### Data from 2001
* Daily_Lstaion_Final_0806.csv: Ridership+Weather, the input to build BSTS
* Other mobility data can be found at:
https://data.covid.umd.edu/
* COVID-19 cases data can be download from:
https://coronavirus.jhu.edu/us-map

### Data from 2015
* Daily_Lstaion_Final.csv: Ridership+Weather, the input to build BSTS


## Code
* 1-Data_Prepare.py: Finish the data preprocessing.
* 2-SEM_Fit.R: Build the dynamic SEM model in R.
* 3-Plot.py: Visualize the results.
* Optimal_Lag.R: Find the optimal lag for SEM models.
* Prediction_Compare.R: Compare the model performance with/without mobility features, also commpare the prediction performance of different models.
* SEM_IN_PYTHON.py: A similar SEM model fit processing in Python.
* SEM_PANEL.R: Build a mixed-effect panel model with SEM structure.

## Methodology
To capture the time-varying relationship between the number of infection and mobility inflow, we have developed a simultaneous equations model with time-varying coefficients. The main results are reported in the main manuscripts, while the details are reported in the supplementary, including:
* Details of mobility metrics
* Number of New cases and Inflow varying in reopen states 
* Optimal Lag
* Model performance 
* Model Interpretation
* Other methods: BSTS 
* Other variables: the risked inflow

