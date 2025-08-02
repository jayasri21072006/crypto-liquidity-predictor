import streamlit as st
import joblib
import pandas as pd
import os

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
model = joblib.load(model_path)

st.title("🪙 Crypto Liquidity Predictor")
st.markdown("Enter the crypto market data to predict **liquidity level**:")

# Collect user inputs
features = {
    'Open': st.number_input('Open Price', value=0.0),
    'High': st.number_input('High Price', value=0.0),
    'Low': st.number_input('Low Price', value=0.0),
    'Close': st.number_input('Close Price', value=0.0),
    'Volume': st.number_input('Volume', value=0.0),
    'Market Cap': st.number_input('Market Cap', value=0.0),
    'SMA_5': st.number_input('SMA_5', value=0.0),
    'EMA_12': st.number_input('EMA_12', value=0.0),
    'RSI': st.number_input('RSI', value=0.0),
    'MACD': st.number_input('MACD', value=0.0)
}

# Convert to DataFrame
input_df = pd.DataFrame(features, index=[0])

# Prediction Logic
def classify_liquidity(value):
    if value < 0.4:
        return "Low 🟥"
    elif value < 0.7:
        return "Medium 🟨"
    else:
        return "High 🟩"

# Button to trigger prediction
if st.button("🔍 Predict Liquidity"):
    try:
        prediction = model.predict(input_df)[0]
        level = classify_liquidity(prediction)
        st.success(f"💧 Predicted Liquidity Score: **{prediction:.2f}**")
        st.info(f"📊 Liquidity Level: **{level}**")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")




