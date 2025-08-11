import streamlit as st
import joblib
import pandas as pd
import os
import matplotlib.pyplot as plt

# 🎯 Load ML Model
model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
model = joblib.load(model_path)

# 🌈 Streamlit Page Setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# 💅 Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #00e6e6;
            text-align: center;
        }
        .section {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# 📌 Title
st.markdown("<div class='main-title'>💧 Crypto Liquidity Predictor</div>", unsafe_allow_html=True)

# 📄 Disclaimer
agree = st.checkbox("I understand this is a prediction tool and may not be accurate.")

# 📥 User Inputs
st.markdown("<div class='section'><h3>📥 Enter Crypto Data</h3></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    volume = st.number_input("Trading Volume", min_value=0.0, format="%.2f")
    open_price = st.number_input("Open Price", min_value=0.0, format="%.2f")
    close_price = st.number_input("Close Price", min_value=0.0, format="%.2f")
with col2:
    high_price = st.number_input("High Price", min_value=0.0, format="%.2f")
    low_price = st.number_input("Low Price", min_value=0.0, format="%.2f")
    market_cap = st.number_input("Market Cap", min_value=0.0, format="%.2f")

# 🧠 Prepare data for prediction
input_data = pd.DataFrame({
    'Volume': [volume],
    'Open': [open_price],
    'Close': [close_price],
    'High': [high_price],
    'Low': [low_price],
    'MarketCap': [market_cap]
})

# 📌 Function to classify liquidity
def classify_liquidity(score):
    if score >= 0.75:
        return "High Liquidity"
    elif score >= 0.5:
        return "Moderate Liquidity"
    else:
        return "Low Liquidity"

# 📌 Function to guess trend
def predict_price_trend(open_p, close_p):
    if close_p > open_p:
        return "Uptrend 📈"
    elif close_p < open_p:
        return "Downtrend 📉"
    else:
        return "No Change ➖"

# 🔮 Predict Button
if st.button("🔍 Predict Liquidity", help="Click to generate prediction"):
    if agree:
        try:
            # Prediction
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)

            # Display prediction results
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

            # 🎯 Histogram representation
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.hist([score], bins=10, range=(0, 1), color='skyblue', edgecolor='black')
            ax.axvline(score, color='red', linestyle='--', linewidth=2, label=f'Score: {score:.2f}')
            ax.set_title("Liquidity Score Histogram")
            ax.set_xlabel("Score Range")
            ax.set_ylabel("Frequency")
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
    else:
        st.warning("⚠️ Please accept the disclaimer to use the prediction feature.")
