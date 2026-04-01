from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np

# Initialize the API
app = FastAPI(
    title="GEOAPI: Petrophysical Predictive API",
    description="API for predicting Deep Resistivity (RESD) from well log data."
)

# Load the models
# If you saved them in one dictionary, adjust the loading logic accordingly.
try:
    with open("scaler.pkl", "rb") as file:
        scaler = pickle.load(file)
    with open("best_model.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    print("Error: Ensure models are in the same directory.")

# Define the expected input schema using Pydantic
class WellLogFeatures(BaseModel):
    CALI: float
    DT: float
    GR: float
    LLS: float
    NPHI: float
    RHOB: float
    DEPT: float


@app.post("/predict")
def predict_resistivity(features: WellLogFeatures):
    try:
        '''1. Convert the incoming JSON into a Pandas DataFrame 
        (This is to ensures feature names match what the scaler/model expects)
        '''
        input_data = pd.DataFrame([features.model_dump()])
        
        # 2. Transform the data using the loaded scaler
        scaled_input = scaler.transform(input_data)
        
        # Model predicts log(1 + RESD)
        log_prediction = model.predict(scaled_input)
        # Back-transform to ohm.m
        prediction_actual = np.expm1(log_prediction)[0]
            
        return {
            "status": "success",
            "predicted_RESD": round(float(prediction_actual), 2)
                }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))