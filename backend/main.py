from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
from preprocessing import preprocess_input

app = FastAPI(title="Diabetes Risk Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_methods=["*"],
    allow_headers=["*"],
)

dt_model = joblib.load("models/decision_tree_diabetes_model.pkl")
lr_model = joblib.load("models/logistic_regression_diabetes_model.pkl")

class PatientInput(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

# Simple root endpoint
@app.get("/")
def root():
    return {"message": "Diabetes Risk Prediction API"}

# POST predict endpoint with validation
@app.post("/predict")
def predict(data: PatientInput):
    input_data = data.dict()

    # -------------------------
    # VALIDATION
    # -------------------------
    if input_data["Pregnancies"] < 0:
        raise HTTPException(status_code=400, detail="Pregnancies cannot be negative.")
    if input_data["Glucose"] <= 0:
        raise HTTPException(status_code=400, detail="Glucose must be greater than 0.")
    if input_data["BloodPressure"] <= 0:
        raise HTTPException(status_code=400, detail="Blood Pressure must be greater than 0.")
    if input_data["SkinThickness"] <= 0:
        raise HTTPException(status_code=400, detail="Skin Thickness must be greater than 0.")
    if input_data["Insulin"] <= 0:
        raise HTTPException(status_code=400, detail="Insulin must be greater than 0.")
    if input_data["BMI"] <= 0:
        raise HTTPException(status_code=400, detail="BMI must be greater than 0.")
    if input_data["DiabetesPedigreeFunction"] <= 0:
        raise HTTPException(status_code=400, detail="Diabetes Pedigree Function must be greater than 0.")
    if input_data["Age"] <= 0:
        raise HTTPException(status_code=400, detail="Age must be greater than 0.")

    # -------------------------
    # PREPROCESS AND PREDICT
    # -------------------------
    df_input, df_scaled = preprocess_input(input_data)

    dt_pred = int(dt_model.predict(df_input)[0])
    lr_pred = int(lr_model.predict(df_scaled)[0])

    return {
        "decision_tree_prediction": "Diabetic" if dt_pred == 1 else "Non-Diabetic",
        "logistic_regression_prediction": "Diabetic" if lr_pred == 1 else "Non-Diabetic"
    }
