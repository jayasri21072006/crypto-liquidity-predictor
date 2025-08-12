import streamlit as st
import joblib
import pandas as pd
import os

# --- Load your navbar HTML ---
def load_navbar():
    with open("crypto_navbar.html", "r", encoding="utf-8") as f:
        return f.read()

# Load ML Model
try:
    model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading the model: {e}")

# Page Setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# Render Navbar
navbar_html = load_navbar()
st.components.v1.html(navbar_html, height=110, scrolling=False)

# Add some spacing after navbar to separate content
st.markdown("<br><br>", unsafe_allow_html=True)

# Title & Subtitle with spacing and styling
st.markdown(
    "<div style='margin-bottom: 10px; font-size: 24px; font-weight: 600;'>Crypto Liquidity Predictor</div>", 
    unsafe_allow_html=True
)
st.markdown(
    "<div style='margin-bottom: 30px; font-size: 16px;'>Enter crypto data to estimate <strong>Liquidity Level</strong>.</div>", 
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# Initialize session state for inputs on first run or demo load
for key in ["open_price", "high_price", "low_price", "close_price", "volume"]:
    if key not in st.session_state:
        st.session_state[key] = 0.0

# Demo data function
def load_demo_data():
    st.session_state.open_price = 56787.5
    st.session_state.high_price = 64776.4
    st.session_state.low_price = 55000.0
    st.session_state.close_price = 63000.0
    st.session_state.volume = 123456.789

# Demo data button
if st.button("Load Demo Data"):
    load_demo_data()

# User Inputs with Market Cap shown below Low Price
col1, col2 = st.columns(2)
with col1:
    open_price = st.number_input(
        'Open Price', value=st.session_state.open_price, format="%.4f",
        help="The price at which the cryptocurrency opened during the trading period."
    )
    high_price = st.number_input(
        'High Price', value=st.session_state.high_price, format="%.4f",
        help="The highest price the cryptocurrency reached during the trading period."
    )
    low_price = st.number_input(
        'Low Price', value=st.session_state.low_price, format="%.4f",
        help="The lowest price the cryptocurrency reached during the trading period."
    )
with col2:
    close_price = st.number_input(
        'Close Price', value=st.session_state.close_price, format="%.4f",
        help="The price at which the cryptocurrency closed during the trading period."
    )
    volume = st.number_input(
        'Volume', value=st.session_state.volume, format="%.4f",
        help="The total amount of cryptocurrency traded during the trading period."
    )

market_cap = close_price * volume

# Show Market Cap below Low Price input in col1 as readonly text (using st.markdown)
st.markdown(f"""
    <div style="margin-top: 8px; font-weight: bold;">
        Auto-calculated Market Cap: <span style="color:#0044cc;">${market_cap:,.2f}</span>
    </div>
""", unsafe_allow_html=True)

# Price Overview Chart
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

# Custom CSS for results and disclaimer
st.markdown("""
    <style>
    .result-high {
        color: #00c853;
        font-weight: bold;
    }
    .result-medium {
        color: #ffca28;
        font-weight: bold;
    }
    .result-low {
        color: #d50000;
        font-weight: bold;
    }
    .disclaimer {
        background-color: #fff4e6;
        border-left: 6px solid #ff9800;
        padding: 15px;
        border-radius: 10px;
        margin-top: 30px;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

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
            <div style='text-align:center; margin-top: 20px;'>
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
<hr>
<p style='text-align:center; font-size:14px; color:grey;'>
    Made with ❤️ by Coinsight ML team · Version 1.0 · Not financial advice
</p>
""", unsafe_allow_html=True)
