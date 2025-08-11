import streamlit as st
import joblib
import pandas as pd
import os

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
    .result-high { color: #00c853; font-weight: bold; }
    .result-medium { color: #ffca28; font-weight: bold; }
    .result-low { color: #d50000; font-weight: bold; }
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #ffe4ec;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #444;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #fff8f0;
        border-radius: 8px;
        color: #ff4081;
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

# ⚠️ Disclaimer
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ Disclaimer:</strong><br>
    This tool uses an AI/ML model to make predictions based on input data.<br>
    <b>We do not guarantee accuracy</b>, and <b>we are not responsible for any financial losses</b>.
</div>
""", unsafe_allow_html=True)

agree = st.checkbox("✅ I acknowledge and accept the disclaimer above.")

# 🚀 Predict Button
if st.button("🔍 Predict Liquidity", help="Click to generate prediction"):
    if agree:
        try:
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)

            # 🎯 Show prediction results
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

            # 📚 Tabs with extra info
            tab1, tab2 = st.tabs(["💡 What is Crypto?", "❓ Q&A"])

            with tab1:
                st.markdown("""
                ### 🪙 What is Cryptocurrency?
                Cryptocurrency is a digital or virtual form of money that uses cryptography for security.  
                It operates on decentralized blockchain technology.

                **Popular Coins:**
                - **Bitcoin (BTC)** – The first and largest cryptocurrency.
                - **Ethereum (ETH)** – Known for smart contracts.
                - **Binance Coin (BNB)** – Used on Binance exchange.
                - **Cardano (ADA)** – Energy-efficient blockchain platform.
                """)

            with tab2:
                st.markdown("""
                ### ❓ Frequently Asked Questions

                **Q1: Is this prediction 100% accurate?**  
                📝 No. The prediction is based on historical data patterns and may not always be correct.

                **Q2: Should I invest based on this tool?**  
                📝 Always do your own research and consult financial advisors before investing.

                **Q3: How is liquidity important?**  
                📝 Liquidity determines how easily an asset can be bought or sold without affecting its price.
                """)

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
    else:
        st.warning("⚠️ Please accept the disclaimer to use the prediction feature.")

