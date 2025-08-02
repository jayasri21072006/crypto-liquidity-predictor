import streamlit as st
import joblib
import pandas as pd
import os

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
model = joblib.load(model_path)

st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="🪙")
st.title("🪙 Crypto Liquidity Predictor")
st.markdown("Enter the crypto market data to predict **liquidity level**.")

st.markdown("---")

# Input fields with tooltips
features = {
    'Open': st.number_input('Open Price', value=0.0, help="Opening price of the cryptocurrency on the day."),
    'High': st.number_input('High Price', value=0.0, help="Highest price of the cryptocurrency for the day."),
    'Low': st.number_input('Low Price', value=0.0, help="Lowest price of the cryptocurrency for the day."),
    'Close': st.number_input('Close Price', value=0.0, help="Closing price of the cryptocurrency on the day."),
    'Volume': st.number_input('Volume', value=0.0, help="Total traded volume (number of coins/tokens)."),
    'Market Cap': st.number_input('Market Cap', value=0.0, help="Market capitalization = Price × Circulating supply."),
    'SMA_5': st.number_input('SMA (5-day)', value=0.0, help="Simple Moving Average over last 5 days."),
    'EMA_12': st.number_input('EMA (12-day)', value=0.0, help="Exponential Moving Average over last 12 days."),
    'RSI': st.number_input('RSI', value=0.0, help="Relative Strength Index (0–100), shows momentum strength."),
    'MACD': st.number_input('MACD', value=0.0, help="Moving Average Convergence Divergence – trend indicator.")
}

# Convert input to DataFrame
input_df = pd.DataFrame(features, index=[0])

# Liquidity classification logic
def classify_liquidity(value):
    if value < 0.4:
        return "Low 🟥"
    elif value < 0.7:
        return "Medium 🟨"
    else:
        return "High 🟩"

# Predict button
if st.button("🔍 Predict Liquidity"):
    try:
        prediction = model.predict(input_df)[0]
        level = classify_liquidity(prediction)
        st.success(f"💧 Predicted Liquidity Score: **{prediction:.2f}**")
        st.info(f"📊 Liquidity Level: **{level}**")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")






