import streamlit as st
import joblib
import pandas as pd
import os

@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
    return joblib.load(model_path)

model = load_model()

st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# ... your CSS and title here ...

with st.form("input_form"):
    open_price = st.number_input('Open Price', value=0.0, format="%.4f")
    high_price = st.number_input('High Price', value=0.0, format="%.4f")
    low_price = st.number_input('Low Price', value=0.0, format="%.4f")
    close_price = st.number_input('Close Price', value=0.0, format="%.4f")
    volume = st.number_input('Volume', value=0.0, format="%.4f")
    submitted = st.form_submit_button("Predict Liquidity")

market_cap = close_price * volume

if submitted:
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
    if st.checkbox("I acknowledge and accept the disclaimer above."):
        try:
            score = model.predict(input_data)[0]
            # your classify_liquidity and prediction display code here
        except Exception as e:
            st.error(f"Prediction failed: {e}")
    else:
        st.warning("Please accept the disclaimer to proceed.")

# Market cap display below low price (outside form)
st.markdown(f"<div>Auto-calculated Market Cap: ${market_cap:,.2f}</div>", unsafe_allow_html=True)
