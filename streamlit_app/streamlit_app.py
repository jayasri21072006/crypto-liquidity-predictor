import streamlit as st
import joblib
import pandas as pd
import os

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
model = joblib.load(model_path)

# Page setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="🪙")
st.title("🪙 Crypto Liquidity Predictor")
st.markdown("Use this tool to **predict the liquidity level** of a cryptocurrency based on market data.")

st.markdown("---")
st.header("📥 Input Market Data")

# Input fields (interactive with help tooltips)
features = {
    'Open': st.number_input('🔓 Open Price', value=0.0, step=0.01, help="Opening price of the cryptocurrency on the day."),
    'High': st.number_input('📈 High Price', value=0.0, step=0.01, help="Highest price of the cryptocurrency for the day."),
    'Low': st.number_input('📉 Low Price', value=0.0, step=0.01, help="Lowest price of the cryptocurrency for the day."),
    'Close': st.number_input('🔐 Close Price', value=0.0, step=0.01, help="Closing price of the cryptocurrency on the day."),
    'Volume': st.number_input('📊 Volume', value=0.0, step=0.01, help="Total traded volume (number of coins/tokens)."),
    'Market Cap': st.number_input('💰 Market Cap', value=0.0, step=0.01, help="Market capitalization = Price × Circulating supply."),
    'SMA_5': st.number_input('📏 SMA (5-day)', value=0.0, step=0.01, help="Simple Moving Average over last 5 days."),
    'EMA_12': st.number_input('📐 EMA (12-day)', value=0.0, step=0.01, help="Exponential Moving Average over last 12 days."),
    'RSI': st.number_input('📌 RSI (0–100)', value=0.0, step=0.01, help="Relative Strength Index, indicates momentum."),
    'MACD': st.number_input('📎 MACD', value=0.0, step=0.01, help="Moving Average Convergence Divergence.")
}

# Convert input to DataFrame
input_df = pd.DataFrame(features, index=[0])

# Function to classify liquidity
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

        st.success(f"💧 **Predicted Liquidity Score:** `{prediction:.2f}`")
        st.info(f"📊 **Liquidity Level:** `{level}`")

        # Optional: Add a nice visual bar chart
        st.markdown("### 📈 Prediction Summary")
        st.progress(min(int(prediction * 100), 100))

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")

# Footer
st.markdown("---")
st.caption("🔒 Your data is safe and never stored. Model predictions are made locally.")






