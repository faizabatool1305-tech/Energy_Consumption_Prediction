
import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

st.set_page_config(
    page_title="Energy Consumption Prediction",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ Energy Consumption Prediction")
st.write("Predict the next hour's average electricity demand.")

@st.cache_resource
def load_model():
    return joblib.load("energy_consumption_model.pkl")

model = load_model()

st.subheader("Enter Electricity Consumption Data")
st.caption("Enter power measurements in kW.")

current_power = st.number_input(
    "Current Hour Average Power (kW)",
    min_value=0.0, value=1.5
)

lag_1 = st.number_input(
    "Previous Hour Power (kW)",
    min_value=0.0, value=1.4
)

lag_2 = st.number_input(
    "Power 2 Hours Ago (kW)",
    min_value=0.0, value=1.3
)

lag_24 = st.number_input(
    "Power 24 Hours Ago (kW)",
    min_value=0.0, value=1.2
)

rolling_mean = st.number_input(
    "Average Power of Previous 24 Hours (kW)",
    min_value=0.0, value=1.3
)

prediction_time = st.date_input(
    "Date of Current Measurement",
    value=datetime.today()
)

hour = st.slider("Current Hour", 0, 23, 12)

if st.button("Predict Energy Consumption"):
    input_data = pd.DataFrame([{
        "Global_active_power": current_power,
        "lag_1": lag_1,
        "lag_2": lag_2,
        "lag_24": lag_24,
        "rolling_mean_24": rolling_mean,
        "hour": hour,
        "day_of_week": prediction_time.weekday(),
        "month": prediction_time.month
    }])

    prediction = model.predict(input_data)[0]

    st.success(
        f"Predicted Next Hour Average Power: {prediction:.3f} kW"
    )
