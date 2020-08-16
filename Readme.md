# Who's Left Riding Transit During COVID-19? A Joint Modeling Using Bayesian Structural Time-Series and Partial Least Squares Regression
### Songhua Hu, Peng Chen 

## Data
### Data from 2001
* Daily_Lstaion_Final_0806.csv: Ridership+Weather, the input to build BSTS.
* finalMatrix_Transit_0810.csv: Predict results from BSTS
* finalCoeff_Transit_0810.csv: Coeff from BSTS
* finalImpact_Transit_0810.csv: Causal Impact from BSTS [Describe impact based on this file]


### Data from 2015
* Daily_Lstaion_Final.csv: Ridership+Weather, the input to build BSTS.
* finalImpact_Transit_0810_old.csv: Causal Impact from BSTS [Describe p-value of impact based on this file]
* Impact_Sta.csv: impact of each station
* All_final_Transit_R_0812.csv: features to build PLS


## Code
* 1-L_Station_Ridership_Prepare.py: Finish the time-series preprocessing.
* 2-BSTS_Causal_Impact.R: Build the BSTS and infer the causal impact.
* 3-EDA_BSTS_Result.py: Visualize the results from BSTS.
* 4-Feature_Build.py: Build the features matrix for PLS models.
* 5-PLS_Build.R: Finish the PLS model fit.

