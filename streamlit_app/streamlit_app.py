import streamlit as st
import pandas as pd
import numpy as np
import pickle

# --- Load your ML model ---
@st.cache_data
def load_model():
    try:
        with open('crypto_liquidity_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except:
        # Dummy model: returns random liquidity score between 0 and 1
        import random
        class DummyModel:
            def predict(self, X):
                return [random.uniform(0, 1) for _ in range(len(X))]
        return DummyModel()

model = load_model()

# CSS for tooltip style
st.markdown("""
<style>
.tooltip {
  position: relative;
  display: inline-block;
  cursor: help;
  color: #0d6efd;
  font-weight: bold;
  margin-left: 5px;
}
.tooltip .tooltiptext {
  visibility: hidden;
  width: 220px;
  background-color: #555;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 5px 10px;
  position: absolute;
  z-index: 1;
  bottom: 125%; 
  left: 50%;
  margin-left: -110px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 12px;
}
.tooltip .tooltiptext::after {
  content: "";
  position: absolute;
  top: 100%; 
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #555 transparent transparent transparent;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>
""", unsafe_allow_html=True)

def label_with_tooltip(label, tooltip_text):
    return f"""
    <span>{label}
        <span class="tooltip">?
            <span class="tooltiptext">{tooltip_text}</span>
        </span>
    </span>
    """

st.title("Crypto Liquidity Predictor")

# Coin selection (optional)
coin = st.selectbox(
    "Select a Coin (optional)",
    options=["", "Bitcoin (BTC)", "Ethereum (ETH)", "Cardano (ADA)", "Dogecoin (DOGE)"]
)

# Demo data loader
def load_demo():
    return {
        "open": 32000,
        "high": 33000,
        "low": 31000,
        "close": 32500,
        "volume": 45000
    }

if st.button("Load Demo Data"):
    demo = load_demo()
else:
    demo = {"open": 0.0, "high": 0.0, "low": 0.0, "close": 0.0, "volume": 0.0}

# Inputs with tooltips
open_price = st.number_input(
    label=label_with_tooltip("Open Price", "Price at market open."),
    min_value=0.0, value=demo["open"], format="%.4f", step=0.01, key="open"
)
high_price = st.number_input(
    label=label_with_tooltip("High Price", "Highest price in the period."),
    min_value=0.0, value=demo["high"], format="%.4f", step=0.01, key="high"
)
low_price = st.number_input(
    label=label_with_tooltip("Low Price", "Lowest price in the period."),
    min_value=0.0, value=demo["low"], format="%.4f", step=0.01, key="low"
)
close_price = st.number_input(
    label=label_with_tooltip("Close Price", "Price at market close."),
    min_value=0.0, value=demo["close"], format="%.4f", step=0.01, key="close"
)
volume = st.number_input(
    label=label_with_tooltip("Volume", "Traded units during the period."),
    min_value=0.0, value=demo["volume"], format="%.4f", step=0.01, key="volume"
)

market_cap = close_price * volume
st.markdown(f"**Estimated Market Cap:** ${market_cap:,.2f}")

# Prepare input for model
features = pd.DataFrame({
    'Open': [open_price],
    'High': [high_price],
    'Low': [low_price],
    'Close': [close_price],
    'Volume': [volume],
    'Market Cap': [market_cap],
    # Dummy features, add real indicators if needed
    'SMA_5': [0],
    'EMA_12': [0],
    'RSI': [0],
    'MACD': [0]
})

# Predict button
if st.button("Predict Liquidity Level"):
    pred_score = model.predict(features)[0]
    if pred_score < 0.4:
        level = "Low Liquidity"
        color = "red"
    elif pred_score < 0.7:
        level = "Medium Liquidity"
        color = "orange"
    else:
        level = "High Liquidity"
        color = "green"

    st.markdown(f"<h3 style='color:{color};'>Liquidity Prediction: {level} (Score: {pred_score:.2f})</h3>", unsafe_allow_html=True)

    # Show simple line chart for prices
    sample_dates = pd.date_range(end=pd.Timestamp.today(), periods=10)
    sample_data = pd.DataFrame({
        "Open": np.linspace(open_price * 0.9, open_price * 1.1, 10),
        "High": np.linspace(high_price * 0.95, high_price * 1.1, 10),
        "Low": np.linspace(low_price * 0.85, low_price * 1.05, 10),
        "Close": np.linspace(close_price * 0.9, close_price * 1.1, 10),
    }, index=sample_dates)

    st.line_chart(sample_data)

st.markdown("""
---
**Disclaimer:**  
This tool is for educational purposes and provides an estimate based on input data and a model.  
Not financial advice. Please do your own research.
""")
