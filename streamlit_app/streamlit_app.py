import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import os

# ——— Navbar HTML (unchanged) ———
navbar_html = """... your existing navbar HTML ..."""

def load_model():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'crypto_liquidity_model.pkl')
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")
components.html(navbar_html, height=80, scrolling=False)

# ——— Global CSS (unchanged) ———
st.markdown("""... your existing CSS ...""", unsafe_allow_html=True)

st.markdown("<div class='title'>Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter crypto data to estimate <strong>Liquidity Level</strong>.</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ——— Coin Selection ———
coin_names = sorted([
    'Bitcoin', 'Ethereum', 'Tether', 'BNB', 'XRP', 'Solana', 'Cardano',
    'Dogecoin', 'Shiba Inu', 'Polygon', 'Litecoin', 'Polkadot', 'Avalanche',
    'Uniswap', 'Chainlink', 'Stellar', 'VeChain', 'TRON', 'Filecoin', 'Near',
])

# Using Trust Wallet Assets for coin logos
coin_logo_base = "https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/{chain}/info/logo.png"
coin_to_chain = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Tether": "tether",
    "BNB": "binance",   # BNB chain (BNB)
    "XRP": "ripple",
    "Solana": "solana",
    "Cardano": "cardano",
    # Add additional mappings as needed
}

selected_coin = st.selectbox(
    "Optional: Select a Coin Name",
    [""] + coin_names,
    index=0,
    help="Start typing to select a coin from the list."
)

if selected_coin and selected_coin in coin_to_chain:
    chain_name = coin_to_chain[selected_coin]
    logo_url = coin_logo_base.format(chain=chain_name)
    st.markdown(
        f"<img class='background-watermark' src='{logo_url}' alt='{selected_coin} logo'>",
        unsafe_allow_html=True
    )

# ——— Inputs and Session State ———
for key in ['open_price', 'high_price', 'low_price', 'close_price', 'volume']:
    st.session_state.setdefault(key, 0.0)

def load_demo_data():
    st.session_state.open_price = 56787.5
    st.session_state.high_price = 64776.4
    st.session_state.low_price = 55000.0
    st.session_state.close_price = 63000.0
    st.session_state.volume = 123456.789

if st.button("Load Demo Data"):
    load_demo_data()

col1, col2 = st.columns(2)
with col1:
    open_price = st.number_input('Open Price', value=st.session_state.open_price, format="%.4f")
    high_price = st.number_input('High Price', value=st.session_state.high_price, format="%.4f")
    low_price = st.number_input('Low Price', value=st.session_state.low_price, format="%.4f")
    market_cap = close_price = st.session_state.close_price * st.session_state.volume
    st.markdown(f"""
    <div style="margin-top: 10px; font-weight: bold; font-size: 16px;">
        Auto-calculated Market Cap:<br>
        <span style="color:#0044cc;">${market_cap:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    close_price = st.number_input('Close Price', value=st.session_state.close_price, format="%.4f")
    volume = st.number_input('Volume', value=st.session_state.volume, format="%.4f")

# Update session state
for key, val in zip(['open_price','high_price','low_price','close_price','volume'],
                    [open_price, high_price, low_price, close_price, volume]):
    st.session_state[key] = val

price_df = pd.DataFrame({
    "Price": [open_price, high_price, low_price, close_price]
}, index=["Open", "High", "Low", "Close"])
st.markdown("### Price Overview")
st.line_chart(price_df)

input_data = pd.DataFrame({
    'Open': [open_price],
    'High': [high_price],
    'Low': [low_price],
    'Close': [close_price],
    'Volume': [volume],
    'Market Cap': [close_price * volume],
    'SMA_5': [0],
    'EMA_12': [0],
    'RSI': [0],
    'MACD': [0]
})

model = load_model()

def classify_liquidity(score):
    return (
        "<span class='result-low'>Low</span>" if score < 0.4
        else "<span class='result-medium'>Medium</span>" if score < 0.7
        else "<span class='result-high'>High</span>"
    )

def predict_price_trend(open_p, close_p):
    return ("Price may go Up" if close_p > open_p
            else "Price may go Down" if close_p < open_p
            else "No Clear Price Movement")

st.markdown("""
<div class="disclaimer" style="font-size: 14px;">
    <strong>Disclaimer:</strong><br>
    This tool uses an AI/ML model to make predictions based on input data.<br>
    Predictions are not guaranteed for any particular cryptocurrency or token.<br>
    No guarantees are made about accuracy or reliability. Use at your own risk.<br>
    Coin logos provided by Trust Wallet Assets (MIT‑licensed, open‑source).
</div>
""", unsafe_allow_html=True)

agree = st.checkbox("I acknowledge and accept the disclaimer above.")

if st.button("Predict Liquidity"):
    if not model:
        st.error("Model not loaded. Prediction unavailable.")
    elif not agree:
        st.warning("Please accept the disclaimer to proceed.")
    else:
        try:
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)
            st.markdown(f"""
            <div class='section' style='text-align:center'>
                <h2>Prediction Result</h2>
                <p><strong>Selected Coin:</strong> {selected_coin if selected_coin else "N/A"}</p>
                <p><strong>Liquidity Score:</strong> {score:.2f}</p>
                <p><strong>Liquidity Level:</strong> {liquidity_level}</p>
                <p><strong>Price Trend:</strong> {trend}</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
