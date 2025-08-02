import streamlit as st
import joblib
import pandas as pd
import os

# Load the trained model (Make sure the file path is correct relative to where the app runs)
model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
model = joblib.load(model_path)

st.title("🪙 Crypto Liquidity Predictor")

st.markdown("Enter the crypto market data to predict liquidity:")

# Input fields for all 10 features
open_val = st.number_input('Open Price', value=0.0)
high_val = st.number_input('High Price', value=0.0)
low_val = st.number_input('Low Price', value=0.0)
close_val = st.number_input('Close Price', value=0.0)
volume_val = st.number_input('Volume', value=0.0)
market_cap_val = st.number_input('Market Cap', value=0.0)
sma5_val = st.number_input('SMA_5', value=0.0)
ema12_val = st.number_input('EMA_12', value=0.0)
rsi_val = st.number_input('RSI', value=0.0)
macd_val = st.number_input('MACD', value=0.0)

# Prepare input data exactly as per model's training format
input_data = pd.DataFrame([{
    'Open': open_val,
    'High': high_val,
    'Low': low_val,
    'Close': close_val,
    'Volume': volume_val,
    'Market Cap': market_cap_val,
    'SMA_5': sma5_val,
    'EMA_12': ema12_val,
    'RSI': rsi_val,
    'MACD': macd_val
}])

# Prediction
if st.button("Predict Liquidity"):
    try:
        prediction = model.predict(input_data)[0]
        st.success(f"💧 Predicted Liquidity: **{prediction:.2f}**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")



