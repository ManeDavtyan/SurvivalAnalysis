# Survival Analysis and CLV Calculation using AFT models

## Overview

This repository contains a Jupyter notebook and py files analyzing customer churn in a telecommunications dataset. Additionally, it calculates Customer Lifetime Value (CLV) and estimates an annual retention budget, suggesting ideas for customer retention.

## Methods Used

- **Data Preparation:** Categorical variables are transformed, and the dataset is preprocessed for survival analysis.

- **AFT Models:** Accelerated Failure Time models (Weibull, Exponential, LogNormal, LogLogistic) are implemented to predict survival times.

- **Model Selection:** The LogNormal AFT model is chosen based on AIC and BIC values.

- **CLV Calculation:** Survival probabilities from the LogNormal AFT model are utilized to compute CLV for each customer.

- **Visualization:** Visualizations of CLV distributions are provided across customer categories, marital status, and regions.

- **Estimated Annual Retention Budget:** An estimated annual retention budget is calculated based on CLV and survival probabilities.

## How to Use?
1. **clone repository to your local device**
2. **install requirnments.txt file in a newly created venv**
3. **run .py file to see the working graphs and analyses**
4. **run .ipynb file to read the notes and comments alongside**


