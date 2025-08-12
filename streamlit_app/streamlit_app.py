import streamlit as st
import joblib
import pandas as pd
import os

# Load ML Model
try:
    model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading the model: {e}")

# Page Setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="wide")

# --- Custom CSS mimicking your site style ---
st.markdown("""
<style>
/* Body background */
body {
    background-color: #0e1a3d;
    color: #f0f0f0;
}

/* Header */
header {
    background-color: #172a6b;
    padding: 15px 30px;
    border-bottom: 3px solid #5c85d6;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Title */
.title {
    font-size: 38px;
    font-weight: 700;
    color: #5c85d6;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    font-size: 18px;
    color: #cfd9f8;
    margin-bottom: 20px;
}

/* Button style */
.stButton > button {
    background-color: #3358f4;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 8px 25px;
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #527bff;
}

/* Input boxes */
div[data-baseweb="select"] > div {
    background-color: #1c2a6f !important;
    color: white !important;
}
input[type=number] {
    background-color: #1c2a6f !important;
    color: white !important;
    border-radius: 6px;
    padding-left: 8px;
}

/* Cards and sections */
.section {
    background-color: #172a6b;
    border-radius: 12px;
    padding: 25px;
    margin-top: 20px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.35);
}

/* Result styles */
.result-high {
    color: #4caf50;
    font-weight: 700;
}
.result-medium {
    color: #ffeb3b;
    font-weight: 700;
}
.result-low {
    color: #f44336;
    font-weight: 700;
}

/* Disclaimer box */
.disclaimer {
    background-color: #223466;
    border-left: 6px solid #5c85d6;
    padding: 15px;
    border-radius: 8px;
    font-size: 16px;
    margin: 30px 0;
    color: #b0b9d7;
}

/* Market cap info */
.market-cap {
    font-weight: 600;
    color: #a3c5ff;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

# Header (custom, since Streamlit doesn't have a fixed header)
st.markdown("""
<header>
    <div class="title">CryptoPredictions.com</div>
    <div class="subtitle">Predict Liquidity Levels with AI/ML — Powered by Coinsight ML Team</div>
</header>
""", unsafe_allow_html=True)

# Main app content in a centered container
st.markdown("<div class='section'>", unsafe_allow_html=True)

# Demo data flag
if 'demo_loaded' not in st.session_state:
    st.session_state.demo_loaded = False

demo_data = {
    "Open Price": 29400.1234,
    "High Price": 29750.5678,
    "Low Price": 29050.4321,
    "Close Price": 29600.7890,
    "Volume": 1200.5678
}

# Load Demo Data Button
if st.button("Load Demo Data for Bitcoin"):
    st.session_state.demo_loaded = True

# Input defaults
def_val = lambda key: demo_data[key] if st.session_state.demo_loaded else 0.0

open_price = st.number_input("Open Price", value=def_val("Open Price"), format="%.4f")
high_price = st.number_input("High Price", value=def_val("High Price"), format="%.4f")
low_price = st.number_input("Low Price", value=def_val("Low Price"), format="%.4f")
close_price = st.number_input("Close Price", value=def_val("Close Price"), format="%.4f")
volume = st.number_input("Volume", value=def_val("Volume"), format="%.4f")

market_cap = close_price * volume

st.markdown(f"<div class='market-cap'>Auto-calculated Market Cap: ${market_cap:,.2f}</div>", unsafe_allow_html=True)

# Price overview chart
price_df = pd.DataFrame({
    "Price": [open_price, high_price, low_price, close_price]
}, index=["Open", "High", "Low", "Close"])
st.markdown("### Price Overview")
st.line_chart(price_df)

# Prepare input data
input_data = pd.DataFrame({
    'Open': [open_price],
    'High': [high_price],
    'Low': [low_price],
    'Close': [close_price],
    'Volume': [volume],
    'Market Cap': [market_cap],
    # Placeholder indicators - replace with your real data or calculations
    'SMA_5': [0],
    'EMA_12': [0],
    'RSI': [0],
    'MACD': [0]
})

def classify_liquidity(score):
    if score < 0.4:
        return "<span class='result-low'>Low</span>"
    elif score < 0.7:
        return "<span class='result-medium'>Medium</span>"
    else:
        return "<span class='result-high'>High</span>"

def predict_price_trend(open_price, close_price):
    if close_price > open_price:
        return "Price may go Up"
    elif close_price < open_price:
        return "Price may go Down"
    else:
        return "No Clear Price Movement"

# Disclaimer
st.markdown("""
<div class="disclaimer">
    <strong>Disclaimer:</strong><br>
    This tool uses an AI/ML model to make predictions based on input data.<br>
    No guarantees are made about accuracy or reliability. Use at your own risk.
</div>
""", unsafe_allow_html=True)

agree = st.checkbox("I acknowledge and accept the disclaimer above.")

if st.button("Predict Liquidity"):
    if agree:
        try:
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)
            st.markdown(f"""
            <div style="text-align:center; margin-top: 30px;">
                <h2>Prediction Result</h2>
                <p><strong>Liquidity Score:</strong> {score:.2f}</p>
                <p><strong>Liquidity Level:</strong> {liquidity_level}</p>
                <p><strong>Price Trend:</strong> {trend}</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
    else:
        st.warning("Please accept the disclaimer to proceed.")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<hr style="border-color:#3358f4;">
<p style='text-align:center; font-size:14px; color:#a3b5ff; margin-top:20px;'>
    Made with ❤️ by Coinsight ML team · Version 1.0 · Not financial advice
</p>
""", unsafe_allow_html=True)
