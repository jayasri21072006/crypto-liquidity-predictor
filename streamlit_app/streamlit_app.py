import streamlit as st
import joblib
import pandas as pd
import os

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
model = joblib.load(model_path)

st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="🪙")
st.title("🪙 Crypto Liquidity Predictor")
st.markdown("Enter the crypto market data to predict **liquidity level**.")

st.markdown("---")

# Input fields with tooltips
features = {
    'Open': st.number_input('💰 Open Price', value=0.0, help="Opening price of the cryptocurrency on the day."),
    'High': st.number_input('📈 High Price', value=0.0, help="Highest price of the cryptocurrency for the day."),
    'Low': st.number_input('📉 Low Price', value=0.0, help="Lowest price of the cryptocurrency for the day."),
    'Close': st.number_input('🔒 Close Price', value=0.0, help="Closing price of the cryptocurrency on the day."),
    'Volume': st.number_input('🔄 Volume', value=0.0, help="Total traded volume (number of coins/tokens)."),
    'Market Cap': st.number_input('🏦 Market Cap', value=0.0, help="Market capitalization = Price × Circulating supply."),
    'SMA_5': st.number_input('📊 SMA (5-day)', value=0.0, help="Simple Moving Average over last 5 days."),
    'EMA_12': st.number_input('📉 EMA (12-day)', value=0.0, help="Exponential Moving Average over last 12 days."),
    'RSI': st.number_input('📊 RSI', value=0.0, help="Relative Strength Index (0–100), shows momentum strength."),
    'MACD': st.number_input('🧮 MACD', value=0.0, help="Moving Average Convergence Divergence – trend indicator.")
}

# Convert input to DataFrame
input_df = pd.DataFrame(features, index=[0])

# Liquidity classification logic
def classify_liquidity(value):
    if value < 0.4:
        return "Low 🟥"
    elif value < 0.7:
        return "Medium 🟨"
    else:
        return "High 🟩"

# Prediction & Display
if st.button("🔍 Predict Liquidity"):
    try:
        prediction = model.predict(input_df)[0]
        level = classify_liquidity(prediction)

        st.success("✅ Prediction Successful!")
        st.markdown(f"### 📈 Prediction Summary")
        col1, col2 = st.columns(2)
        col1.metric("💧 Liquidity Score", f"{prediction:.2f}")
        col2.metric("📊 Liquidity Level", level)

        with st.expander("ℹ️ What does this mean?"):
            if "Low" in level:
                st.warning("🔻 **Low Liquidity** means the asset may be hard to trade quickly without affecting its price. Use caution.")
            elif "Medium" in level:
                st.info("🟡 **Medium Liquidity** indicates a balanced state. Trading is possible with moderate impact.")
            else:
                st.success("🟢 **High Liquidity** means the asset is easy to trade and very active in the market.")

        st.markdown("---")

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")







