import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import os

# --- Navbar HTML ---
navbar_html = """
<nav style="background-color:#102a44; color:white; display:flex; align-items:center; padding:12px 30px; justify-content:space-between; border-radius:0 0 10px 10px; box-shadow:0 4px 8px rgba(0,0,0,0.1); font-family: 'Poppins', Arial, sans-serif; width: 100vw; position: fixed; top: 0; left: 0; z-index: 9999; box-sizing: border-box;">
  <div style="display:flex; align-items:center;">
    <div style="font-weight:700; font-size:26px; background: linear-gradient(90deg, #34e89e, #0f3443); -webkit-background-clip: text; -webkit-text-fill-color: transparent; user-select:none; cursor:default;">CryptoPredictions</div>
  </div>
  <ul class="nav-links" style="list-style:none; display:flex; gap: 25px; margin:0; padding:0;">
    <li><a href="https://cryptonews.com" target="_blank" style="color:white; text-decoration:none; font-weight:600;">Market Updates</a></li>
    <li><a href="https://cryptopredictions.com/?results=200" target="_blank" style="color:white; text-decoration:none; font-weight:600;">Coin List</a></li>
    <li><a href="https://cryptopredictions.com/blog/" target="_blank" style="color:white; text-decoration:none; font-weight:600;">Insights Blog</a></li>
  </ul>
  <div style="display:flex; align-items:center; gap:20px;">
    <div>
      <a href="https://twitter.com" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" style="width:24px; height:24px;"></a>
      <a href="https://facebook.com" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" style="width:24px; height:24px; margin-left: 10px;"></a>
    </div>
    <select style="background:transparent; border:none; color:white; font-weight:600; font-size:15px;">
      <option value="en" selected>English 🇬🇧</option>
      <option value="es">Español 🇪🇸</option>
      <option value="fr">Français 🇫🇷</option>
    </select>
  </div>
</nav>
"""

# --- Load ML Model ---
def load_model():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'crypto_liquidity_model.pkl')
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# --- Streamlit Setup ---
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")
components.html(navbar_html, height=80, scrolling=False)

# --- Background Image Path (uploaded image) ---
background_img_path = "/mnt/data/f579c044-d998-4ae9-ba04-5b3516794592.png"

# --- CSS Styling with transparent background ---
st.markdown(f"""
<style>
body {{
    padding-top: 80px;
    background-color: transparent;
    background-image: url("{background_img_path}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    font-family: 'Poppins', Arial, sans-serif;
    color: white;
}}

.stApp {{
    background-color: rgba(0, 0, 0, 0.3);
    padding: 30px 40px;
    border-radius: 12px;
    box-shadow: none;
    min-height: 80vh;
    z-index: 2;
    position: relative;
    color: white;
}}

.title, .subtitle, .disclaimer {{
    color: white !important;
}}

.result-high {{
    color: #00ff00;
    font-weight: bold;
}}
.result-medium {{
    color: #ffff00;
    font-weight: bold;
}}
.result-low {{
    color: #ff4444;
    font-weight: bold;
}}
</style>
""", unsafe_allow_html=True)

# --- Title & Subtitle ---
st.markdown("<div class='title'>Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter crypto data to estimate <strong>Liquidity Level</strong>.</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Coin Selector ---
coin_names = sorted([
    'Bitcoin', 'Ethereum', 'Tether', 'BNB', 'XRP', 'Solana', 'Cardano',
    'Dogecoin', 'Shiba Inu', 'Polygon', 'Litecoin', 'Polkadot', 'Avalanche',
    'Uniswap', 'Chainlink', 'Stellar', 'VeChain', 'TRON', 'Filecoin', 'Near',
])

coin_logos = {
    "Bitcoin": "https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=024",
    "Ethereum": "https://cryptologos.cc/logos/ethereum-eth-logo.png?v=024",
    "Tether": "https://cryptologos.cc/logos/tether-usdt-logo.png?v=024",
    "BNB": "https://cryptologos.cc/logos/binance-coin-bnb-logo.png?v=024",
    "XRP": "https://cryptologos.cc/logos/xrp-xrp-logo.png?v=024",
    "Solana": "https://cryptologos.cc/logos/solana-sol-logo.png?v=024",
    "Cardano": "https://cryptologos.cc/logos/cardano-ada-logo.png?v=024"
}

selected_coin = st.selectbox("Optional: Select a Coin Name", [""] + coin_names, index=0)
if selected_coin and selected_coin in coin_logos:
    st.markdown(
        f"<img class='background-watermark' src='{coin_logos[selected_coin]}' alt='Coin logo watermark'>",
        unsafe_allow_html=True
    )

# --- Input Fields Initialization ---
for key in ['open_price', 'high_price', 'low_price', 'close_price', 'volume']:
    if key not in st.session_state:
        st.session_state[key] = 0.0

def load_demo_data():
    st.session_state.open_price = 56787.5
    st.session_state.high_price = 64776.4
    st.session_state.low_price = 55000.0
    st.session_state.close_price = 63000.0
    st.session_state.volume = 123456.789

if st.button("Load Demo Data"):
    load_demo_data()

# --- Input Form ---
col1, col2 = st.columns(2)
with col1:
    open_price = st.number_input('Open Price', value=st.session_state.open_price, format="%.4f")
    high_price = st.number_input('High Price', value=st.session_state.high_price, format="%.4f")
    low_price = st.number_input('Low Price', value=st.session_state.low_price, format="%.4f")

with col2:
    close_price = st.number_input('Close Price', value=st.session_state.close_price, format="%.4f")
    volume = st.number_input('Volume', value=st.session_state.volume, format="%.4f")

# --- Update Session ---
st.session_state.open_price = open_price
st.session_state.high_price = high_price
st.session_state.low_price = low_price
st.session_state.close_price = close_price
st.session_state.volume = volume

# --- Market Cap Calculation ---
market_cap = close_price * volume
st.markdown(f"""<div style="margin-top: 10px; font-weight: bold; font-size: 16px;">Auto-calculated Market Cap:<br><span style="color:#00aaff;">${market_cap:,.2f}</span></div>""", unsafe_allow_html=True)

# --- Price Chart ---
price_df = pd.DataFrame({"Price": [open_price, high_price, low_price, close_price]}, index=["Open", "High", "Low", "Close"])
st.markdown("### Price Overview")
st.line_chart(price_df)

# --- Model Input Format ---
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

# --- Load Model ---
model = load_model()

# --- Classifier Helper Functions ---
def classify_liquidity(score):
    if score < 0.4:
        return "<span class='result-low'>Low</span>"
    elif score < 0.7:
        return "<span class='result-medium'>Medium</span>"
    else:
        return "<span class='result-high'>High</span>"

def predict_price_trend(open_p, close_p):
    if close_p > open_p:
        return "Price may go Up"
    elif close_p < open_p:
        return "Price may go Down"
    else:
        return "No Clear Price Movement"

# --- Disclaimer ---
st.markdown("""
<div class="disclaimer">
    <strong>Disclaimer:</strong><br>
    This tool uses an AI/ML model to make predictions based on input data.<br>
    Predictions are not guaranteed for any particular cryptocurrency or token.<br>
    No guarantees are made about accuracy or reliability. Use at your own risk.
</div>
""", unsafe_allow_html=True)

agree = st.checkbox("I acknowledge and accept the disclaimer above.")

# --- Prediction Button ---
if st.button("Predict Liquidity"):
    if not model:
        st.error("Model not loaded. Prediction unavailable.")
    elif agree:
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
    else:
        st.warning("Please accept the disclaimer to proceed.")
