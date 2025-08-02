import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('crypto_liquidity_model.pkl')

# App title
st.title("💸 Crypto Liquidity Predictor")

# Description
st.markdown("Predict **cryptocurrency liquidity** as 'Low', 'Medium', or 'High' based on real-time market inputs.")

# Input fields for the user
price = st.number_input("Current Price (USD)", value=1000.0)
volume = st.number_input("24h Volume (USD)", value=1_000_000.0)
mkt_cap = st.number_input("Market Cap (USD)", value=100_000_000.0)
change_1h = st.number_input("Change in 1 Hour (%)", value=0.0)
change_24h = st.number_input("Change in 24 Hours (%)", value=0.0)
change_7d = st.number_input("Change in 7 Days (%)", value=0.0)

# Predict button
if st.button("Predict Liquidity"):
    # Prepare input
    input_data = pd.DataFrame([[price, change_1h, change_24h, change_7d, volume, mkt_cap]],
                              columns=['price', '1h', '24h', '7d', '24h_volume', 'mkt_cap'])

    prediction = model.predict(input_data)[0]

    # Classify into categories
    if prediction < 0.4:
        label = "Low"
        color = "red"
    elif prediction < 0.7:
        label = "Medium"
        color = "orange"
    else:
        label = "High"
        color = "green"

    # Show result
    st.markdown(f"### 💧 Predicted Liquidity Level: <span style='color:{color}'><b>{label}</b></span>", unsafe_allow_html=True)
    st.write(f"🔢 Raw Prediction Score: `{prediction:.3f}`")

    st.success(f"Predicted Liquidity Level: **{prediction:.4f}**")
