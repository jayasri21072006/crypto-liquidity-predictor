import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import os

# Navbar
navbar_html = """<nav style="background-color:#102a44;color:white;display:flex;align-items:center;padding:12px 30px;justify-content:space-between;border-radius:0 0 10px 10px;box-shadow:0 4px 8px rgba(0,0,0,0.1);font-family:'Poppins', Arial, sans-serif;width:100vw;position:fixed;top:0;left:0;z-index:9999;box-sizing:border-box;"><div style="display:flex;align-items:center;"><div style="font-weight:700;font-size:26px;background: linear-gradient(90deg, #34e89e, #0f3443); -webkit-background-clip: text;-webkit-text-fill-color: transparent; user-select:none; cursor:default;">CryptoPredictions</div></div><ul class="nav-links" style="list-style:none;display:flex;gap: 25px;margin:0;padding:0;"><li><a href="https://cryptonews.com" target="_blank" rel="noopener noreferrer" style="color:white;text-decoration:none;font-weight:600;">Market Updates</a></li><li><a href="https://cryptopredictions.com/?results=200" target="_blank" rel="noopener noreferrer" style="color:white;text-decoration:none;font-weight:600;">Coin List</a></li><li><a href="https://cryptopredictions.com/blog/" target="_blank" rel="noopener noreferrer" style="color:white;text-decoration:none;font-weight:600;">Insights Blog</a></li></ul><div style="display:flex;align-items:center;gap:20px;"><div><a href="https://twitter.com" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="Twitter" style="width:24px;height:24px;"></a><a href="https://facebook.com" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook" style="width:24px;height:24px;margin-left: 10px;"></a></div><select style="background:transparent;border:none;color:white;font-weight:600;font-size:15px;cursor:pointer;padding:4px;border-radius:4px;"><option value="en" selected>English 🇬🇧</option><option value="es">Español 🇪🇸</option><option value="fr">Français 🇫🇷</option></select></div></nav>"""

st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")
components.html(navbar_html, height=80, scrolling=False)

# --- CSS ---
st.markdown("""
<style>
body {
    padding-top: 80px;
    background-color: #f9fafb;
    font-family: 'Poppins', Arial, sans-serif;
    color: #102a44;
}
.stApp {
    background-color: rgba(255, 255, 255, 0.95);
    padding: 30px 40px;
    border-radius: 12px;
    box-shadow: 0 8px 30px rgba(16, 42, 68, 0.1);
    position: relative;
    min-height: 80vh;
}
.background-watermark {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 250px;
    height: 250px;
    opacity: 0.08;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 0;
}
.title {
    text-align: center;
    color: #0044cc;
    font-size: 50px;
    font-weight: bold;
    margin-top: 15px;
    z-index: 1;
    position: relative;
}
.subtitle {
    text-align: center;
    color: #333;
    font-size: 20px;
    margin-bottom: 20px;
    z-index: 1;
    position: relative;
}
.section {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
    margin-top: 20px;
    position: relative;
    z-index: 1;
}
.disclaimer {
    background-color: #fff4e6;
    border-left: 6px solid #ff9800;
    padding: 15px;
    border-radius: 10px;
    margin-top: 30px;
    font-size: 14px;
    position: relative;
    z-index: 1;
}
.result-high {
    color: #00c853;
    font-weight: bold;
}
.result-medium {
    color: #ffca28;
    font-weight: bold;
}
.result-low {
    color: #d50000;
    font-weight: bold;
}
.stNumberInput > div > input {
    background-color: #fff !important;
    color: #102a44 !important;
    border: 1.5px solid #cdd9e5;
    border-radius: 6px;
    padding: 8px;
}
.stButton > button {
    background-color: #4ca1af;
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #397f86;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<div class='title'>Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter crypto data to estimate <strong>Liquidity Level</strong>.</div>", unsafe_allow_html=True)

# --- Coin Selection ---
coin_names = ['Bitcoin', 'Ethereum', 'Tether', 'BNB', 'XRP', 'Solana', 'Cardano']
coin_to_chain = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Tether": "tether",
    "BNB": "binance",
    "XRP": "ripple",
    "Solana": "solana",
    "Cardano": "cardano"
}
coin_logo_base = "https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/{chain}/info/logo.png"
selected_coin = st.selectbox("Optional: Select a Coin Name", [""] + coin_names)

if selected_coin in coin_to_chain:
    chain = coin_to_chain[selected_coin]
    logo_url = coin_logo_base.format(chain=chain)
    st.markdown(f"<img class='background-watermark' src='{logo_url}'>", unsafe_allow_html=True)

# --- Input ---
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
    open_price = st.number_input("Open Price", value=st.session_state.open_price)
    high_price = st.number_input("High Price", value=st.session_state.high_price)
    low_price = st.number_input("Low Price", value=st.session_state.low_price)
with col2:
    close_price = st.number_input("Close Price", value=st.session_state.close_price)
    volume = st.number_input("Volume", value=st.session_state.volume)

market_cap = close_price * volume
st.markdown(f"<div style='font-weight:bold;'>Market Cap: ${market_cap:,.2f}</div>", unsafe_allow_html=True)

price_df = pd.DataFrame({
    "Price": [open_price, high_price, low_price, close_price]
}, index=["Open", "High", "Low", "Close"])
st.line_chart(price_df)

# --- Load Model ---
def load_model():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return joblib.load(os.path.join(script_dir, 'crypto_liquidity_model.pkl'))
    except Exception as e:
        st.error(f"Model load error: {e}")
        return None

model = load_model()

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

def classify_liquidity(score):
    if score < 0.4:
        return "<span class='result-low'>Low</span>"
    elif score < 0.7:
        return "<span class='result-medium'>Medium</span>"
    return "<span class='result-high'>High</span>"

def predict_price_trend(open_p, close_p):
    return "Price may go Up" if close_p > open_p else "Price may go Down" if close_p < open_p else "No Clear Price Movement"

st.markdown("""
<div class="disclaimer"><strong>Disclaimer:</strong> This tool uses AI to estimate liquidity. It does not provide financial advice. Use at your own risk.</div>
""", unsafe_allow_html=True)

agree = st.checkbox("I acknowledge and accept the disclaimer above.")

if st.button("Predict Liquidity"):
    if not model:
        st.error("Model not loaded.")
    elif not agree:
        st.warning("Please accept the disclaimer to continue.")
    else:
        try:
            score = model.predict(input_data)[0]
            liquidity = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)

            st.markdown(f"""
            <div class='section' style='text-align:center'>
                <h2>Prediction Result</h2>
                <p><strong>Selected Coin:</strong> {selected_coin if selected_coin else "N/A"}</p>
                <p><strong>Liquidity Score:</strong> {score:.2f}</p>
                <p><strong>Liquidity Level:</strong> {liquidity}</p>
                <p><strong>Price Trend:</strong> {trend}</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction error: {e}")
