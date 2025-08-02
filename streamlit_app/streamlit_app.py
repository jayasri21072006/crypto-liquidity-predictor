import streamlit as st
import pandas as pd
import joblib
import os

# Load trained model
model = joblib.load(os.path.join("crypto_liquidity_model.pkl"))

# Define expected features (same order used during training)
expected_features = [
    'price_usd', 'market_cap', 'volume_24h', 'btc_dominance',
    'eth_dominance', 'active_addresses',
    'feature_7', 'feature_8', 'feature_9', 'feature_10'  # placeholder names
]

# Streamlit UI
st.title("Crypto Liquidity Predictor")

# Input form
price_usd = st.number_input("Price (USD)")
market_cap = st.number_input("Market Cap")
volume_24h = st.number_input("24h Volume")
btc_dominance = st.number_input("BTC Dominance (%)")
eth_dominance = st.number_input("ETH Dominance (%)")
active_addresses = st.number_input("Active Addresses")

# Optional: Add UI for feature_7 to feature_10 if values are known
# For now, default to 0
feature_7 = 0
feature_8 = 0
feature_9 = 0
feature_10 = 0

# Predict button
if st.button("Predict Liquidity"):
    input_data = pd.DataFrame([[
        price_usd, market_cap, volume_24h, btc_dominance, eth_dominance, active_addresses,
        feature_7, feature_8, feature_9, feature_10
    ]], columns=expected_features)

    prediction = model.predict(input_data)[0]
    st.success(f"Predicted Liquidity: {prediction:.2f}")


