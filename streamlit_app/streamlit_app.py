import streamlit as st
import joblib
import pandas as pd
import os

# Set page config FIRST, before any other Streamlit commands
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# 🎯 Load ML Model with Error Handling
try:
    model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading the model: {e}")

# 💅 Custom CSS Styling with Gradient Background and Hover Effects
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #ff6f61, #ffb3ba);
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        text-align: center;
        color: #0044cc;
        font-size: 50px;
        font-weight: bold;
        margin-top: 15px;
    }
    .subtitle {
        text-align: center;
        color: #333;
        font-size: 20px;
        margin-bottom: 20px;
    }
    .section {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        transition: 0.3s;
    }
    .section:hover {
        transform: scale(1.02);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.15);
    }
    .disclaimer {
        background-color: #fff4e6;
        border-left: 6px solid #ff9800;
        padding: 15px;
        border-radius: 10px;
        margin-top: 30px;
        font-size: 18px;
    }
    .result-high {
        color: #00c853;
        font-weight: bold;
        transition: 0.3s;
    }
    .result-medium {
        color: #ffca28;
        font-weight: bold;
        transition: 0.3s;
    }
    .result-low {
        color: #d50000;
        font-weight: bold;
        transition: 0.3s;
    }
    .result-high:hover {
        color: #00c853;
        text-shadow: 0 0 15px #00c853;
    }
    .result-medium:hover {
        color: #ffca28;
        text-shadow: 0 0 10px #ffca28;
    }
    .result-low:hover {
        color: #d50000;
        text-shadow: 0 0 10px #d50000;
    }
    .button:hover {
        background-color: #ff9800;
        box-shadow: 0px 4px 15px rgba(255, 152, 0, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Title & Subtitle
st.markdown("<div class='title'>Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter key crypto data to estimate <strong>Liquidity Level</strong>.</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# User Inputs Section
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        open_price = st.number_input('Open Price', value=0.0, format="%.4f")
        high_price = st.number_input('High Price', value=0.0, format="%.4f")
        low_price = st.number_input('Low Price', value=0.0, format="%.4f")
        # Show Market Cap below Low Price (auto-calculated)
        market_cap = 0.0  # Initialize here
    with col2:
        close_price = st.number_input('Close Price', value=0.0, format="%.4f")
        volume = st.number_input('Volume', value=0.0, format="%.4f")

# Calculate Market Cap after inputs
market_cap = close_price * volume

# Show Market Cap below Low Price
st.markdown(f"""
<div class="section">
    <b>Auto-Calculated Market Cap:</b> ${market_cap:,.2f}
</div>
""", unsafe_allow_html=True)

# Prepare input for prediction (exclude Market Cap from prediction features)
input_data = pd.DataFrame({
    'Open': [open_price],
    'High': [high_price],
    'Low': [low_price],
    'Close': [close_price],
    'Volume': [volume],
    # 'Market Cap' excluded from prediction inputs
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

# Disclaimer Acknowledgment
agree = st.checkbox("I acknowledge and accept the disclaimer above.")

# Predict Button
st.markdown("<br>", unsafe_allow_html=True)

if st.button("Predict Liquidity"):
    if agree:
        try:
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)

            # Show Prediction Results WITHOUT market cap in prediction
            st.markdown(f"""
            <div class='section'>
                <h3>Prediction Result</h3>
                <ul>
                    <li>Liquidity Score: {score:.2f}</li>
                    <li>Liquidity Level: {liquidity_level}</li>
                    <li>Price Trend Hint: {trend}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Prediction failed: {e}")
    else:
        st.warning("Please accept the disclaimer to use the prediction feature.")

# Footer
st.markdown("""
    <div style="text-align:center; margin-top:40px; font-size:12px; color:#999;">
    Made with ❤️ by Coinsight ML Team · Version 1.0 · Not financial advice
    </div>
""", unsafe_allow_html=True)
