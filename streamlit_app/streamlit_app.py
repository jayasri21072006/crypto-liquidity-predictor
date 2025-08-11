import streamlit as st
import joblib
import pandas as pd
import os

# 🎯 Load ML Model
model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
model = joblib.load(model_path)

# 🌈 Streamlit Page Setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# 💅 Custom CSS Styling
st.markdown("""
    <style>
    body {
        background-color: #f0f7ff;
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        text-align: center;
        color: #0077ff;
        font-size: 50px;
        font-weight: bold;
        margin-top: 15px;
    }
    .subtitle {
        text-align: center;
        color: #333;
        font-size: 20px;
        margin-bottom: 10px;
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
        transform: scale(1.01);
        box-shadow: 0px 8px 18px rgba(0, 0, 0, 0.15);
    }
    .disclaimer {
        background-color: #fff4e6;
        border-left: 6px solid #ff9800;
        padding: 15px;
        border-radius: 10px;
        margin-top: 30px;
    }
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
    </style>
""", unsafe_allow_html=True)

# 🪙 Title & Subtitle
st.markdown("<div class='title'>🪙 Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter key crypto data to estimate <strong>Liquidity Level</strong>.</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ✏️ User Inputs Section
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        open_price = st.number_input('🔓 Open Price', value=0.0, format="%.4f")
        high_price = st.number_input('🔺 High Price', value=0.0, format="%.4f")
        low_price = st.number_input('🔻 Low Price', value=0.0, format="%.4f")
    with col2:
        close_price = st.number_input('🔒 Close Price', value=0.0, format="%.4f")
        volume = st.number_input('📦 Volume', value=0.0, format="%.4f")

# 💰 Auto-calculate Market Cap
market_cap = close_price * volume

# 🧾 Show calculated Market Cap
st.markdown(f"""
<div class="section">
    💰 <b>Auto-Calculated Market Cap:</b> <code>{market_cap:,.2f}</code>
</div>
""", unsafe_allow_html=True)

# 🧠 Prepare input for prediction
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

# 🔍 Classification logic
def classify_liquidity(score):
    if score < 0.4:
        return "<span class='result-low'>🟥 Low</span>"
    elif score < 0.7:
        return "<span class='result-medium'>🟨 Medium</span>"
    else:
        return "<span class='result-high'>🟩 High</span>"

def predict_price_trend(open_price, close_price):
    if close_price > open_price:
        return "📈 Price may go Up"
    elif close_price < open_price:
        return "📉 Price may go Down"
    else:
        return "❓ No Clear Price Movement"

# ⚠️ Disclaimer section
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ Disclaimer:</strong> <br>
    This application is built for <b>educational and experimental purposes only</b>. <br>
    Predictions are based on historical indicators via a machine learning model. <br>
    These are <b>not financial advice</b> and we <b>do not guarantee</b> accuracy. <br>
    We <b>do not provide suggestions</b> for any specific coin, token, or investment. <br>
    <br>
    <i>By using this app, you acknowledge and accept these terms.</i>
</div>
""", unsafe_allow_html=True)

agree = st.checkbox("✅ I acknowledge and accept the disclaimer above.")

# 🚀 Predict Button
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔍 Predict Liquidity", help="Click to generate prediction"):
    if agree:
        try:
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)

            # 🎯 Show results
            st.markdown(f"""
            <div class='section'>
                <h3>📊 Prediction Result</h3>
                <ul>
                    <li>💧 <b>Liquidity Score</b>: {score:.2f}</li>
                    <li>🔵 <b>Liquidity Level</b>: {liquidity_level}</li>
                    <li>📉 <b>Price Trend Hint</b>: {trend}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
    else:
        st.warning("⚠️ Please accept the disclaimer to use the prediction feature.")