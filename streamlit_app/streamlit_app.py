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
    .title { text-align: center; color: #0044cc; font-size: 50px; font-weight: bold; margin-top: 15px; }
    .subtitle { text-align: center; color: #333; font-size: 20px; margin-bottom: 20px; }
    .section { background-color: #ffffff; border-radius: 15px; padding: 20px;
               box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1); margin-top: 20px; }
    .disclaimer { background-color: #fff4e6; border-left: 6px solid #ff9800; padding: 15px; border-radius: 10px; }
    .result-high { color: #00c853; font-weight: bold; }
    .result-medium { color: #ffca28; font-weight: bold; }
    .result-low { color: #d50000; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 🪙 Title & Subtitle
st.markdown("<div class='title'>🪙 Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter key crypto data to estimate <strong>Liquidity Level</strong>.</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ✏️ User Inputs
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
st.markdown(f"<div class='section'>💰 <b>Market Cap:</b> {market_cap:,.2f}</div>", unsafe_allow_html=True)

# 🧠 Match training feature order
try:
    if hasattr(model, "feature_names_in_"):
        feature_order = list(model.feature_names_in_)
    else:
        # Fallback: define manually based on training
        feature_order = ['Open', 'High', 'Low', 'Close', 'Volume',
                         'Market Cap', 'SMA_5', 'EMA_12', 'RSI', 'MACD']

    # Fill missing features with 0
    input_dict = {
        'Open': open_price,
        'High': high_price,
        'Low': low_price,
        'Close': close_price,
        'Volume': volume,
        'Market Cap': market_cap,
        'SMA_5': 0,
        'EMA_12': 0,
        'RSI': 0,
        'MACD': 0
    }

    input_data = pd.DataFrame([[input_dict[feat] for feat in feature_order]], columns=feature_order)

except Exception as e:
    st.error(f"Feature alignment error: {e}")
    st.stop()

# 🔍 Classification logic
def classify_liquidity(score):
    if score < 0.4: return "<span class='result-low'>🟥 Low</span>"
    elif score < 0.7: return "<span class='result-medium'>🟨 Medium</span>"
    else: return "<span class='result-high'>🟩 High</span>"

def predict_price_trend(open_p, close_p):
    if close_p > open_p: return "📈 Price may go Up"
    elif close_p < open_p: return "📉 Price may go Down"
    else: return "❓ No Clear Movement"

# ⚠️ Disclaimer
st.markdown("""
<div class="disclaimer">
    <b>⚠️ Disclaimer:</b> This tool uses an AI/ML model and is not financial advice.
</div>
""", unsafe_allow_html=True)
agree = st.checkbox("✅ I understand and accept")

# 🚀 Predict
if st.button("🔍 Predict Liquidity"):
    if agree:
        try:
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)

            st.markdown(f"""
            <div class='section'>
                <h3>📊 Prediction Result</h3>
                💧 <b>Score:</b> {score:.2f} <br>
                🔵 <b>Level:</b> {liquidity_level} <br>
                📉 <b>Trend:</b> {trend}
            </div>
            """, unsafe_allow_html=True)

            # 📝 Question & Solution section
            with st.expander("💡 Common Questions & Answers"):
                st.write("**Q: How is liquidity calculated?**")
                st.write("**A:** The model uses price, volume, and indicators like SMA, EMA, RSI, and MACD.")
                st.write("**Q: Can this predict future prices?**")
                st.write("**A:** No, it estimates liquidity conditions, not exact prices.")
                st.write("**Q: Is this financial advice?**")
                st.write("**A:** No, please do your own research.")

        except Exception as e:
            st.error(f"Prediction failed: {e}")
    else:
        st.warning("Please accept the disclaimer first.")

