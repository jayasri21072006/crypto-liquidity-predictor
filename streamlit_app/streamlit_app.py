import streamlit as st
import joblib
import pandas as pd
import os

# 🧠 Load your trained ML model
model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
model = joblib.load(model_path)

# 📄 Streamlit page setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# 🪙 Title & Subtitle
st.markdown("""
    <h1 style='text-align: center; color: #00BFFF;'>🪙 Crypto Liquidity Predictor</h1>
    <p style='text-align: center;'>Enter key crypto data to estimate <strong>Liquidity Level</strong>.</p>
    <hr>
""", unsafe_allow_html=True)

# ✏️ Inputs: you enter crypto info
col1, col2 = st.columns(2)
with col1:
    open_price = st.number_input('🔓 Open Price', value=0.0)
    high_price = st.number_input('🔺 High Price', value=0.0)
    low_price = st.number_input('🔻 Low Price', value=0.0)
with col2:
    close_price = st.number_input('🔒 Close Price', value=0.0)
    volume = st.number_input('📦 Volume', value=0.0)
    market_cap = st.number_input('💰 Market Cap', value=0.0, help="Market capitalization = Price × Circulating supply.")

# 📦 Prepare data like a lunchbox for ML model
input_data = pd.DataFrame({
    'Open': [open_price],
    'High': [high_price],
    'Low': [low_price],
    'Close': [close_price],
    'Volume': [volume],
    'Market Cap': [market_cap],
    'SMA_5': [0],     # 📉 Calculated internally in model or not used
    'EMA_12': [0],
    'RSI': [0],
    'MACD': [0]
})

# 📊 Liquidity classification
def classify_liquidity(score):
    if score < 0.4:
        return "🟥 Low"
    elif score < 0.7:
        return "🟨 Medium"
    else:
        return "🟩 High"

# 📈 Price trend estimate
def predict_price_trend(open_price, close_price):
    if close_price > open_price:
        return "📈 Price may go Up"
    elif close_price < open_price:
        return "📉 Price may go Down"
    else:
        return "❓ No Clear Price Movement"

# 🔘 Predict button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 Predict Liquidity"):
    try:
        score = model.predict(input_data)[0]
        liquidity_level = classify_liquidity(score)
        trend = predict_price_trend(open_price, close_price)

        # ✅ Show result
        st.markdown(f"""
        ### 📊 Prediction Result

        - 💧 **Liquidity Score**: {score:.2f}  
        - 🔵 **Liquidity Level**: {liquidity_level}  
        - 📉 **Price Trend Hint**: {trend}  
        """, unsafe_allow_html=True)

        # ⚠️ Disclaimer
        st.markdown("""
        ---
        **🔒 Disclaimer:**  
        This prediction is based on historical and statistical data using a basic machine learning model.  
        It should NOT be used for financial decisions or investment advice.  
        We are not responsible for any losses or decisions made based on this tool.
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")

