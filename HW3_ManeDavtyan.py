# Importing Libraries
import pandas as pd
import numpy as np
from lifelines import WeibullFitter, ExponentialFitter, LogNormalFitter, LogLogisticFitter, WeibullAFTFitter, LogNormalAFTFitter, LogLogisticAFTFitter
import matplotlib.pyplot as plt
import seaborn as sns

# Data Preparation
telco = pd.read_csv("telco.csv")
telco.head()
telco.dtypes
telco.set_index('ID', inplace=True)
telco['churn'] = pd.Series(np.where(telco.churn.values == "Yes", 1, 0), telco.index)
columns = ['region', 'marital', 'ed', 'retire', 'gender', 'voice', 'internet', 'forward', 'custcat']
telco = pd.get_dummies(telco, columns=columns, prefix=columns, drop_first=True)
telco["tenure"] = np.where(telco["tenure"] == 0, 0.000001, telco["tenure"])

# AFT Models
wf = WeibullFitter()
ef = ExponentialFitter()
lnf = LogNormalFitter()
llf = LogLogisticFitter()

fig, ax = plt.subplots(figsize=(16, 8))
for model in [wf, ef, lnf, llf]:
    model.fit(durations=telco["tenure"], event_observed=telco["churn"])
    model.plot_survival_function()
    print("AIC of", model.__class__.__name__, "model is", model.AIC_)
    print("BIC of", model.__class__.__name__, "model is", model.BIC_)
    model.print_summary()

# Analyzing the winning model
logn_aft = LogNormalAFTFitter()
logn_aft.fit(telco, duration_col='tenure', event_col='churn')
logn_aft.print_summary()

# Coefficient interpretation
# Features with positive coefficients increase the hazard of churn, while negatives lower the hazard of churn.
telco = telco[["tenure", "churn", "address", "age", "custcat_E-service", "custcat_Plus service", "custcat_Total service", "internet_Yes", "marital_Unmarried", "voice_Yes"]]
logn_aft = LogNormalAFTFitter()
logn_aft.fit(telco, duration_col='tenure', event_col='churn')
logn_aft.print_summary()

# Customer Lifetime Value (CLV)
pred_clv = logn_aft.predict_survival_function(telco)

MM = 1300
r = 12
for col in range(1, len(pred.columns)+1):
    for row in range(1, 13):
        pred[col][row] = pred[col][row] / (1 + r / 12)**(row - 1)
telco_orig['CLV'] = MM * pred.sum(axis=0)

# Visualizing CLV across segments
avg_clv_by_category = telco_orig.groupby('custcat')['CLV'].mean()
best_segment = avg_clv_by_category.idxmax()
print(f"The best segment based on average CLV is: {best_segment}")

avg_clv_by_marital = telco_orig.groupby('marital')['CLV'].mean()
best_marital_status = avg_clv_by_marital.idxmax()
print(f"The best segment based on average CLV for marital status is: {best_marital_status}")

avg_clv_by_region = telco_orig.groupby('region')['CLV'].mean()
best_region = avg_clv_by_region.idxmax()
print(f"The best segment based on average CLV for region is: {best_region}")

# Visualizing CLV distributions
plt.figure(figsize=(12, 8))
clv_plot = sns.kdeplot(data=telco_orig, x='CLV', hue='custcat', fill=True, common_norm=False)
plt.title('CLV Distribution Across Customer Categories')
plt.xlabel('Customer Lifetime Value (CLV)')
plt.ylabel('Density')
plt.show()

plt.figure(figsize=(12, 8))
clv_marital_plot = sns.kdeplot(data=telco_orig, x='CLV', hue='marital', fill=True, common_norm=False)
plt.title('CLV Distribution by Marital Status')
plt.xlabel('Customer Lifetime Value (CLV)')
plt.ylabel('Density')
plt.show()

plt.figure(figsize=(12, 8))
clv_region_plot = sns.kdeplot(data=telco_orig, x='CLV', hue='region', fill=True, common_norm=False)
plt.title('CLV Distribution Across Regions')
plt.xlabel('Customer Lifetime Value (CLV)')
plt.ylabel('Density')
plt.show()

# Calculating Annual Retention Budget
r = 0.07
telco_orig['Annual_CLV'] = telco_orig['CLV'] / ((1 + r) ** (telco_orig['tenure'] / 12))
at_risk_customers = telco_orig[telco_orig['CLV'] * pred.iloc[:, 0] < 3000]
retention_budget = at_risk_customers['Annual_CLV'].sum()
print("Estimated Annual Retention Budget: $", round(retention_budget, 2))
