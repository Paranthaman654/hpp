import streamlit as st
import pandas as pd
import numpy as np
import pickle

# --- Load model and features ---
with open("house_price_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model_features.pkl", "rb") as f:
    feature_names = pickle.load(f)

# --- UI ---
st.title("🏠 House Price Prediction App")
st.markdown("Enter house details below to estimate the sale price.")

# --- User Inputs ---
area = st.selectbox("Area", ['Adyar', 'Anna Nagar', 'Chrompet', 'Karapakkam', 'Velachery'])
int_sqft = st.number_input("Interior Sqft", min_value=500, max_value=5000, value=1200)
dist_mainroad = st.slider("Distance to Main Road (m)", 0, 500, 100)
bedroom = st.slider("Number of Bedrooms", 1, 5, 2)
bathroom = st.slider("Number of Bathrooms", 1, 4, 1)
sale_cond = st.selectbox("Sale Condition", ['AbNormal', 'Family', 'Partial', 'AdjLand'])
park = st.selectbox("Parking Facility", ['Yes', 'No'])
buildtype = st.selectbox("Build Type", ['Commercial', 'Others', 'Other'])
street = st.selectbox("Street Type", ['Paved', 'Gravel', 'No Access'])
mzzone = st.selectbox("Municipal Zone", ['A', 'RH', 'RL', 'RM', 'C', 'I'])
age = st.slider("Building Age (years)", 0, 100, 20)
reg_fee = st.number_input("Registration Fee ₹", min_value=10000, max_value=1000000, value=300000)

# --- Convert to input DataFrame ---
input_dict = {
    'INT_SQFT': int_sqft,
    'DIST_MAINROAD': dist_mainroad,
    'N_BEDROOM': bedroom,
    'N_BATHROOM': bathroom,
    'REG_FEE': reg_fee,
    'AGE': age,
    f'AREA_{area}': 1,
    f'SALE_COND_{sale_cond}': 1,
    f'PARK_FACIL_{park}': 1,
    f'BUILDTYPE_{buildtype}': 1,
    f'STREET_{street}': 1,
    f'MZZONE_{mzzone}': 1
}

# Set missing columns to 0
for col in feature_names:
    if col not in input_dict:
        input_dict[col] = 0

input_df = pd.DataFrame([input_dict])[feature_names]

# --- Prediction ---
if st.button("Predict Price"):
    price = model.predict(input_df)[0]
    st.success(f"💰 Estimated Sale Price: ₹{int(price):,}")
