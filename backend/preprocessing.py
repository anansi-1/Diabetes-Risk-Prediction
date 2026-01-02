import pandas as pd
import joblib

scaler = joblib.load("models/scaler.pkl")

cols_with_zero = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI"
]

median_values = {
    "Glucose": 117.0,
    "BloodPressure": 72.0,
    "SkinThickness": 23.0,
    "Insulin": 30.5,
    "BMI": 32.0
}

def preprocess_input(input_data):
    df_input = pd.DataFrame([input_data])

    for col in cols_with_zero:
        if df_input[col].values[0] == 0:
            df_input[col] = median_values[col]

    df_scaled = scaler.transform(df_input)

    return df_input, df_scaled
