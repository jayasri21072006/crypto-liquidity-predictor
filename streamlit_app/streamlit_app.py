import streamlit as st
import joblib
import pandas as pd
import os
import matplotlib.pyplot as plt

# 🎯 Load ML Model with Error Handling
model = None
try:
    model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        st.error(f"❌ Model file not found at: {model_path}")
except Exception as e:
    st.error(f"❌ Error loading the model: {e}")

# 🌈 Streamlit Page Setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# 💅 Custom CSS Styling - ChatGPT Gradient
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #fde2e4, #fad0c4, #fbc2eb, #a6c1ee);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Segoe UI', sans-serif;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
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
        font-size: 26px;
        margin-bottom: 20px;
        font-weight: bold;
    }
    .section {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        transition: 0.3s;
        font-size: 20px;
    }
    .result-box-high {
        background-color: #e6ffed;
        border-left: 8px solid #00c853;
    }
    .result-box-medium {
        background-color: #fffde7;
        border-left: 8px solid #ffca28;
    }
    .result-box-low {
        background-color: #ffebee;
        border-left: 8px solid #d50000;
    }
    label {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #222;
    }
    label[for="🔓 Open Price"],
    label[for="🔺 High Price"],
    label[for="🔻 Low Price"],
    label[for="🔒 Close Price"],
    label[for="📦 Volume"] {
        color: #0044cc !important;
        font-size: 24px !important;
        font-weight: bold !important;
    }
    .disclaimer {
        background-color: #fff4e6;
        border-left: 6px solid #ff9800;
        padding: 15px;
        border-radius: 10px;
        margin-top: 30px;
        font-size: 20px;
        color: orange;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 🪙 Title & Subtitle
st.markdown("<div class='title'>🪙 Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter key crypto data to estimate <strong>Liquidity Level</strong>.</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ✏️ User Inputs
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
st.markdown(f"<div class='section'>💰 <b>Auto-Calculated Market Cap:</b> <code>{market_cap:,.2f}</code></div>", unsafe_allow_html=True)

# 📄 Input Data
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

# 🔍 Classification Logic
def classify_liquidity(score):
    try:
        score = float(score)
    except ValueError:
        return "result-box-low", f"<span style='color:red;'>Invalid score: {score}</span>"
    if score < 0.4:
        return "result-box-low", "<span style='color:red; font-weight:bold;'>🟥 Low</span>"
    elif score < 0.7:
        return "result-box-medium", "<span style='color:orange; font-weight:bold;'>🟨 Medium</span>"
    else:
        return "result-box-high", "<span style='color:green; font-weight:bold;'>🟩 High</span>"

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
    ⚠ Disclaimer:<br>
    This tool uses an AI/ML model to make predictions based on input data.<br>
    We do not guarantee accuracy, and we are not responsible for any financial losses.
</div>
""", unsafe_allow_html=True)

# ✅ Agreement
agree = st.checkbox("✅ I understand the disclaimer", key="agree_checkbox")

# 🚀 Predict
if st.button("🔍 Predict Liquidity"):
    if not agree:
        st.warning("⚠ Please accept the disclaimer to use this feature.")
    elif model is None:
        st.error("❌ No model loaded. Please check the model file.")
    else:
        try:
            raw_output = model.predict(input_data)[0]
            box_class, liquidity_level = classify_liquidity(raw_output)
            trend = predict_price_trend(open_price, close_price)

            st.markdown(f"""
            <div class='section {box_class}'>
                <h3>📊 Prediction Result</h3>
                <ul>
                    <li>💧 <b>Liquidity Score</b>: {raw_output}</li>
                    <li>🔵 <b>Liquidity Level</b>: {liquidity_level}</li>
                    <li>📉 <b>Price Trend Hint</b>: {trend}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            # 📈 Add Graph
            fig, ax = plt.subplots(figsize=(6, 1.2))
            ax.barh(0, raw_output, color='green' if raw_output >= 0.7 else ('orange' if raw_output >= 0.4 else 'red'))
            ax.set_xlim(0, 1)
            ax.set_yticks([])
            ax.set_xlabel("Liquidity Score")
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.set_facecolor("none")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
