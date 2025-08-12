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
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# Dark theme CSS
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #e0e0e0;
    }
    .title {
        text-align: center;
        color: #64b5f6;  /* light blue */
        font-size: 48px;
        font-weight: 700;
        margin-top: 15px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .subtitle {
        text-align: center;
        color: #b0bec5;
        font-size: 20px;
        margin-bottom: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .section {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(100, 181, 246, 0.3);
        margin-top: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #e0e0e0;
    }
    .disclaimer {
        background-color: #263238;
        border-left: 6px solid #fbc02d;
        padding: 15px;
        border-radius: 10px;
        margin-top: 30px;
        font-size: 16px;
        color: #fff9c4;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .result-high {
        color: #81c784; /* soft green */
        font-weight: 600;
    }
    .result-medium {
        color: #ffb74d; /* warm gold */
        font-weight: 600;
    }
    .result-low {
        color: #e57373; /* soft red */
        font-weight: 600;
    }
    /* Market cap text */
    div[style*="Auto-calculated Market Cap"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #90caf9;
    }
    /* Footer styling */
    p {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #90a4ae;
    }
    </style>
""", unsafe_allow_html=True)

# Title & Subtitle without emoji
st.markdown("<div class='title'>Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter crypto data to estimate <strong>Liquidity Level</strong>.</div>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:#64b5f6'>", unsafe_allow_html=True)

# Initialize session state for demo data loading
if 'demo_loaded' not in st.session_state:
    st.session_state.demo_loaded = False

# Demo data example (Bitcoin sample prices)
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

# Set default values based on demo data or zero
default_open = demo_data["Open Price"] if st.session_state.demo_loaded else 0.0
default_high = demo_data["High Price"] if st.session_state.demo_loaded else 0.0
default_low = demo_data["Low Price"] if st.session_state.demo_loaded else 0.0
default_close = demo_data["Close Price"] if st.session_state.demo_loaded else 0.0
default_volume = demo_data["Volume"] if st.session_state.demo_loaded else 0.0

# User Inputs with Market Cap shown below Low Price
col1, col2 = st.columns(2)
with col1:
    open_price = st.number_input(
        'Open Price', value=default_open, format="%.4f",
        help="The price at which the cryptocurrency opened during the trading period."
    )
    high_price = st.number_input(
        'High Price', value=default_high, format="%.4f",
        help="The highest price the cryptocurrency reached during the trading period."
    )
    low_price = st.number_input(
        'Low Price', value=default_low, format="%.4f",
        help="The lowest price the cryptocurrency reached during the trading period."
    )
with col2:
    close_price = st.number_input(
        'Close Price', value=default_close, format="%.4f",
        help="The price at which the cryptocurrency closed during the trading period."
    )
    volume = st.number_input(
        'Volume', value=default_volume, format="%.4f",
        help="The total amount of cryptocurrency traded during the trading period."
    )

market_cap = close_price * volume

# Show Market Cap below Low Price input in col1 as readonly text (using st.markdown)
st.markdown(f"""
    <div style="margin-top: 8px; font-weight: bold;">
        Auto-calculated Market Cap: <span style="color:#64b5f6;">${market_cap:,.2f}</span>
    </div>
""", unsafe_allow_html=True)

# Price Overview Chart (Streamlit default line chart)
price_df = pd.DataFrame({
    "Price": [open_price, high_price, low_price, close_price]
}, index=["Open", "High", "Low", "Close"])
st.markdown("### Price Overview")
st.line_chart(price_df)

# Prepare input data for model
input_data = pd.DataFrame({
    'Open': [open_price],
    'High': [high_price],
    'Low': [low_price],
    'Close': [close_price],
    'Volume': [volume],
    'Market Cap': [market_cap],
    'SMA_5': [0],
    'EMA_12': [0],
    'RSI': [0],
    'MACD': [0]
})

# Classification logic without emojis
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

# Accept disclaimer checkbox
agree = st.checkbox("I acknowledge and accept the disclaimer above.")

# Prediction button
if st.button("Predict Liquidity"):
    if agree:
        try:
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)

            st.markdown(f"""
            <div class='section' style='text-align:center'>
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

# Footer with Coinsight ML team name
st.markdown("""
<hr style="border-color:#64b5f6;">
<p style='text-align:center; font-size:14px; color:#90a4ae;'>
    Made with ❤️ by Coinsight ML team · Version 1.0 · Not financial advice
</p>
""", unsafe_allow_html=True)
