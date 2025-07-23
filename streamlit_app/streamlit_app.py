import streamlit as st
import pandas as pd
import joblib

# ✅ Load the model with full path
model = joblib.load("C:/Users/Jayasri t/streamlit_app/crypto_liquidity_model.pkl")

# App title
st.title("💸 Crypto Liquidity Predictor")

# Description
st.markdown("Predict **cryptocurrency liquidity** based on market conditions.")

# Input fields
price = st.number_input("Current Price (USD)", value=1000.0)
volume = st.number_input("24h Volume (USD)", value=1e6)
mkt_cap = st.number_input("Market Cap (USD)", value=1e8)
change_1h = st.number_input("Change in 1 Hour (%)", value=0.0)
change_24h = st.number_input("Change in 24 Hours (%)", value=0.0)
change_7d = st.number_input("Change in 7 Days (%)", value=0.0)
ma_price = st.number_input("10-day Moving Avg Price", value=1000.0)
ma_volume = st.number_input("10-day Moving Avg Volume", value=1e6)
volatility = st.number_input("Volatility (Std Dev)", value=0.5)
liquidity_ratio = st.number_input("Liquidity Ratio", value=0.01)

# Make a prediction
if st.button("Predict Liquidity"):
    input_data = pd.DataFrame([[price, ma_price, ma_volume, volatility, liquidity_ratio,
                                 change_1h, change_24h, change_7d, volume, mkt_cap]],
                              columns=['price', 'ma_price', 'ma_volume', 'volatility',
                                       'liquidity_ratio', '1h', '24h', '7d',
                                       '24h_volume', 'mkt_cap'])

    prediction = model.predict(input_data)[0]
    st.success(f"📈 Predicted Liquidity Level: **{prediction:.4f}**")
