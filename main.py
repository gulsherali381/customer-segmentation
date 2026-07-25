from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load model aur scaler
model  = joblib.load("kmean.pkl")
scaler = joblib.load("scalar.pkl")

# Segment names
SEGMENTS = {
    0: "VIP",
    1: "Regular",
    2: "Inactive",
    3: "New"
}

# Input ka format
class CustomerData(BaseModel):
    total_spent:     float
    total_orders:    float
    avg_order_value: float
    days_since:      float
    rating:          float

@app.get("/")
def home():
    return {"message": "Customer Segmentation API is running!"}

@app.post("/predict")
def predict(data: CustomerData):
    input_data = np.array([[
        data.total_spent,
        data.total_orders,
        data.avg_order_value,
        data.days_since,
        data.rating
    ]])
    
    input_scaled = scaler.transform(input_data)
    cluster      = int(model.predict(input_scaled)[0])
    segment      = SEGMENTS[cluster]
    
    return {
        "cluster":  cluster,
        "segment":  segment
    }