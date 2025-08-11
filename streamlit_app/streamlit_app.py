import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

# 🎯 Load ML Model
model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
model = joblib.load(model_path)

# 🌈 Streamlit Page Setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# 🖌️ Custom Styling
st.markdown("""
    <style>
    body {
        background-color: #0d0d0d;
        color: white;
    }
    .main {
        background-color: #1a1a1a;
        border-radius: 15px;
        padding: 20px;
    }
    h1, h2, h3 {
        color: #ff6f61;
    }
    </style>
""", unsafe_allow_html=True)

# 📌 Title
st.title("💧 Crypto Liquidity Predictor")

# 📥 Input Section
st.header("Enter Cryptocurrency Data")
open_price = st.number_input("Open Price", min_value=0.0, format="%.2f")
high_price = st.number_input("High Price", min_value=0.0, format="%.2f")
low_price = st.number_input("Low Price", min_value=0.0, format="%.2f")
close_price = st.number_input("Close Price", min_value=0.0, format="%.2f")
volume = st.number_input("Volume", min_value=0.0, format="%.2f")

# Prediction Button
if st.button("Predict Liquidity"):
    input_data = pd.DataFrame({
        "Open": [open_price],
        "High": [high_price],
        "Low": [low_price],
        "Close": [close_price],
        "Volume": [volume]
    })

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.success("✅ High Liquidity Expected")
    else:
        st.error("⚠ Low Liquidity Expected")

# 📊 Show Price Trend Chart (Bar Chart Only)
if open_price > 0 or high_price > 0 or low_price > 0 or close_price > 0:
    fig, ax = plt.subplots(figsize=(6, 4))
    prices = [open_price, high_price, low_price, close_price]
    labels = ["Open", "High", "Low", "Close"]

    ax.bar(labels, prices, color='#ff6f61', alpha=0.8, edgecolor='black')
    ax.set_title("Price Trend", fontsize=16, fontweight='bold', color="#ff6f61")
    ax.set_ylabel("Price", fontsize=12, color="white")
    ax.grid(True, linestyle='--', alpha=0.5, axis='y')
    ax.tick_params(colors='white')
    st.pyplot(fig)

