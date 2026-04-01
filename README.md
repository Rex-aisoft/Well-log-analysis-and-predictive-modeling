## Subsurface Resistivity Prediction: A Petrophysical ML Tool
This project features a machine learning pipeline and a full-stack web application designed to predict Deep Resistivity (RESD) from common well log data. By leveraging a FastAPI backend and an interactive Streamlit frontend, geoscientists can simulate geological scenarios and evaluate formation properties in real-time.

## Overview
Predicting resistivity is a core task in petrophysics used to identify hydrocarbons and evaluate reservoir saturation. This tool uses a Linear Regression model trained on high-quality well log data, incorporating geological domain knowledge such as:

Log-transformation of target variables to handle the exponential nature of resistivity.

IQR-based Outlier Removal to ensure statistical robustness.

Petrophysical Feature Engineering using Gamma Ray, Density, Neutron, and Sonic logs.


## Tech Stack
Language: Python 3.x

Backend: FastAPI (Production-grade API with Pydantic validation)

Frontend: Streamlit (Geoscience-themed interactive UI)

Machine Learning: Scikit-Learn (Linear Regression, StandardScaler)

Data Handling: Pandas, NumPy, LASIO


## Geological Interpretation
The model utilizes specific geophysical logs to derive its predictions:

Gamma Ray (GR): Distinguishes between conductive shales and resistive reservoir sands.

Caliper (CALI): Accounts for borehole stability and washout effects on tool readings.

Density (RHOB) & Neutron (NPHI): Provides information on porosity and fluid content.

Sonic (DT): Relates rock compaction and travel time to electrical tortuosity.