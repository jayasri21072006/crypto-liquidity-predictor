import streamlit as st
import joblib
import pandas as pd
import os
import plotly.graph_objects as go

# 🎯 Load ML Model with Error Handling
try:
    model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading the model: {e}")

# 🌈 Streamlit Page Setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# 💅 Custom CSS Styling
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

# ✨ Use Demo Data Button
if st.button("🧪 Use Demo Data"):
    st.session_state["open_price"] = 100
    st.session_state["high_price"] = 120
    st.session_state["low_price"] = 90
    st.session_state["close_price"] = 110
    st.session_state["volume"] = 5000
    st.experimental_rerun()

# ✏️ User Inputs
col1, col2 = st.columns(2)
with col1:
    open_price = st.number_input('🔓 Open Price', value=st.session_state.get("open_price", 0.0), format="%.4f")
    high_price = st.number_input('🔺 High Price', value=st.session_state.get("high_price", 0.0), format="%.4f")
    low_price = st.number_input('🔻 Low Price', value=st.session_state.get("low_price", 0.0), format="%.4f")
with col2:
    close_price = st.number_input('🔒 Close Price', value=st.session_state.get("close_price", 0.0), format="%.4f")
    volume = st.number_input('📦 Volume', value=st.session_state.get("volume", 0.0), format="%.4f")

# 💰 Auto-calculate Market Cap
market_cap = close_price * volume

# 🧾 Show Market Cap
st.markdown(f"""
<div class="section">
    💰 <b>Auto-Calculated Market Cap:</b> <code>${market_cap:,.2f}</code>
</div>
""", unsafe_allow_html=True)

# 📉 Chart for Price Movement
price_chart = pd.DataFrame({
    "Price Type": ["Open", "High", "Low", "Close"],
    "Price": [open_price, high_price, low_price, close_price]
})
fig = go.Figure(data=[go.Candlestick(
    open=[open_price], high=[high_price], low=[low_price], close=[close_price],
    increasing_line_color='green', decreasing_line_color='red'
)])
fig.update_layout(title="📊 Price Movement", xaxis_title="Time", yaxis_title="Price", height=400)
st.plotly_chart(fig, use_container_width=True)

# 🧠 Input for ML model
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

# 📊 Liquidity Classification
def classify_liquidity(score):
    if score < 0.4:
        return "<span class='result-low'>🟥 Low</span>"
    elif score < 0.7:
        return "<span class='result-medium'>🟨 Medium</span>"
    else:
        return "<span class='result-high'>🟩 High</span>"

# 📈 Price Trend Prediction
def predict_price_trend(open_price, close_price):
    if close_price > open_price:
        return "📈 Price may go Up"
    elif close_price < open_price:
        return "📉 Price may go Down"
    else:
        return "❓ No Clear Price Movement"

# ⚠️ Disclaimer
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ Disclaimer:</strong><br>
    This tool uses an AI/ML model to make predictions based on input data.<br>
    <b>We do not guarantee accuracy</b>, and <b>we are not responsible for any financial losses</b> incurred from using this app.
</div>
""", unsafe_allow_html=True)

# ✅ Disclaimer Acknowledgment
agree = st.checkbox("✅ I acknowledge and accept the disclaimer above.")

# 🚀 Prediction Button
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Predict Liquidity"):
    if agree:
        try:
            # Make prediction
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)

            # 🧾 Show results
            st.markdown(f"""
            <div class='section' style='text-align:center'>
                <h2>🔍 Liquidity Prediction Result</h2>
                <p style='font-size:24px;'>💧 <strong>Liquidity Score:</strong> {score:.2f}</p>
                <p style='font-size:28px;'>🔵 <strong>Liquidity Level:</strong> {liquidity_level}</p>
                <p style='font-size:20px;'>📊 <strong>Market Cap:</strong> ${market_cap:,.2f}</p>
                <p style='font-size:20px;'>📉 <strong>Price Trend Hint:</strong> {trend}</p>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
    else:
        st.warning("⚠️ Please accept the disclaimer to use the prediction feature.")

# 📌 Footer
st.markdown("""
<hr>
<p style='text-align:center; font-size:14px; color:grey;'>
    Made with ❤️ by YourName · Version 1.0 · Not financial advice
</p>
""", unsafe_allow_html=True)
