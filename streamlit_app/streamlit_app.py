import streamlit as st
import joblib
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# 🎯 Load ML Model
model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
model = joblib.load(model_path)

# 🌈 Streamlit Page Setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# 💅 Custom CSS for dark, high-contrast theme
st.markdown(
    """
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-size: 16px;
            font-weight: bold;
        }
        .stTextInput>div>div>input {
            background-color: #1e1e1e;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🖊️ App Title
st.title("💧 Crypto Liquidity Predictor")
st.write("Enter the crypto trading metrics below to predict the **liquidity score**.")

# 📥 Input fields
col1, col2 = st.columns(2)
with col1:
    volume = st.number_input("Trading Volume (24h)", min_value=0.0, format="%.2f")
    market_cap = st.number_input("Market Cap", min_value=0.0, format="%.2f")
    volatility = st.number_input("Volatility Index", min_value=0.0, format="%.2f")
with col2:
    transactions = st.number_input("Number of Transactions", min_value=0)
    price_change = st.number_input("Price Change (%)", format="%.2f")
    spread = st.number_input("Bid-Ask Spread (%)", format="%.2f")

# 📊 Prediction
if st.button("Predict Liquidity"):
    try:
        # Create DataFrame for prediction
        input_df = pd.DataFrame(
            [[volume, market_cap, volatility, transactions, price_change, spread]],
            columns=["volume", "market_cap", "volatility", "transactions", "price_change", "spread"]
        )

        # Get prediction
        prediction = model.predict(input_df)[0]
        
        # Show result
        st.success(f"💹 Predicted Liquidity Score: **{prediction:.2f}**")

        # 📈 Create Gauge-Style Plot
        fig, ax = plt.subplots(figsize=(5, 3), subplot_kw={'projection': 'polar'})
        
        # Normalize prediction for gauge (0-100 scale)
        min_val, max_val = 0, 100
        norm_score = np.clip(prediction, min_val, max_val)
        theta = (1 - (norm_score - min_val) / (max_val - min_val)) * np.pi
        
        # Draw gauge background
        ax.barh(0, np.pi, left=0, height=0.4, color='lightgray')
        ax.barh(0, theta, height=0.4, color='lime' if prediction > 50 else 'orange')
        
        # Style gauge
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_facecolor("#0e1117")
        
        # Display plot
        st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

# ℹ️ Footer
st.markdown("---")
st.markdown("📈 *Powered by Machine Learning & Streamlit*")

