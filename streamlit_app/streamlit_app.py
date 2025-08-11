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
            background-color: #f0f2f6;
        }
        .title {
            font-size: 30px;
            font-weight: bold;
            color: #2e86de;
        }
        .section {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #2e86de;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# 🏷 Title
st.markdown("<div class='title'>💧 Crypto Liquidity Predictor</div>", unsafe_allow_html=True)

# 📌 Input Fields
with st.form("input_form"):
    open_price = st.number_input("📈 Open Price", min_value=0.0, format="%.2f")
    high_price = st.number_input("📊 High Price", min_value=0.0, format="%.2f")
    low_price = st.number_input("📉 Low Price", min_value=0.0, format="%.2f")
    close_price = st.number_input("💵 Close Price", min_value=0.0, format="%.2f")
    volume = st.number_input("📦 Volume", min_value=0.0, format="%.2f")
    market_cap = st.number_input("🏦 Market Cap", min_value=0.0, format="%.2f")

    agree = st.checkbox("✅ I agree this prediction is for educational purposes only")
    submitted = st.form_submit_button("🔍 Predict Liquidity")

# 🔄 Prediction Functions
def classify_liquidity(score):
    if score < 0.4:
        return "Low"
    elif score < 0.7:
        return "Medium"
    else:
        return "High"

def predict_price_trend(open_p, close_p):
    if close_p > open_p:
        return "Uptrend"
    elif close_p < open_p:
        return "Downtrend"
    else:
        return "No Change"

# 🚀 Predict Logic
if submitted:
    if agree:
        try:
            # Prepare input
            input_data = pd.DataFrame([[open_price, high_price, low_price, close_price, volume, market_cap]],
                                      columns=["open", "high", "low", "close", "volume", "market_cap"])

            # Predict
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)

            # 📊 Show Prediction
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

            # 📈 Price Trend Chart
            price_history = [open_price, high_price, low_price, close_price]
            fig, ax = plt.subplots()
            ax.plot(price_history, marker='o', linestyle='-', color='blue')
            ax.set_title("📈 Price Trend (Sample)", fontsize=14, fontweight='bold')
            ax.set_xlabel("Time Step")
            ax.set_ylabel("Price (USD)")
            ax.grid(True, alpha=0.3)

            if close_price > open_price:
                ax.text(len(price_history)-1, close_price, "⬆ Uptrend", color="green", fontsize=12)
            elif close_price < open_price:
                ax.text(len(price_history)-1, close_price, "⬇ Downtrend", color="red", fontsize=12)
            else:
                ax.text(len(price_history)-1, close_price, "➡ No Change", color="orange", fontsize=12)

            st.pyplot(fig)

            # 📊 Liquidity Gauge Chart (Horizontal Bar)
            fig2, ax2 = plt.subplots(figsize=(5, 1.2))
            ax2.barh(["Liquidity"], [score], color=(
                "red" if score < 0.4 else "orange" if score < 0.7 else "green"
            ))
            ax2.set_xlim(0, 1)
            ax2.set_xlabel("Liquidity Score")
            ax2.set_title("💧 Liquidity Level")
            ax2.grid(axis='x', alpha=0.3)
            st.pyplot(fig2)

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
    else:
        st.warning("Please accept the disclaimer before making predictions.")


