import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import os

# Navbar HTML with light theme
navbar_html = """
<nav style="
  background-color:#f5f7fa; 
  color:#102a44; 
  display:flex; 
  align-items:center; 
  padding:12px 30px; 
  justify-content:space-between; 
  border-radius:0 0 10px 10px; 
  box-shadow:0 4px 8px rgba(0,0,0,0.1); 
  font-family: 'Poppins', Arial, sans-serif;
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
  box-sizing: border-box;
">
  <div style="display:flex; align-items:center;">
    <div style="font-weight:700; font-size:26px; background: linear-gradient(90deg, #4ca1af, #c4e0e5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; user-select:none; cursor:default;">CryptoPredictions</div>
  </div>

  <ul class="nav-links" style="list-style:none; display:flex; gap: 25px; margin:0; padding:0;">
    <li><a href="https://cryptonews.com" target="_blank" rel="noopener noreferrer" style="color:#102a44; text-decoration:none; font-weight:600;">Market Updates</a></li>
    <li><a href="https://cryptopredictions.com/?results=200" target="_blank" rel="noopener noreferrer" style="color:#102a44; text-decoration:none; font-weight:600;">Coin List</a></li>
    <li><a href="https://cryptopredictions.com/blog/" target="_blank" rel="noopener noreferrer" style="color:#102a44; text-decoration:none; font-weight:600;">Insights Blog</a></li>
  </ul>

  <div style="display:flex; align-items:center; gap:20px;">
    <div>
      <a href="https://twitter.com" target="_blank" aria-label="Twitter"><img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="Twitter" style="width:24px; height:24px; cursor:pointer; filter:brightness(80%); transition:filter 0.3s ease;"></a>
      <a href="https://facebook.com" target="_blank" aria-label="Facebook"><img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook" style="width:24px; height:24px; cursor:pointer; filter:brightness(80%); transition:filter 0.3s ease; margin-left: 10px;"></a>
    </div>
    <select aria-label="Select Language" style="background:transparent; border:none; color:#102a44; font-weight:600; font-size:15px; cursor:pointer; padding:4px; border-radius:4px; transition:background-color 0.3s ease;">
      <option value="en" selected>English 🇬🇧</option>
      <option value="es">Español 🇪🇸</option>
      <option value="fr">Français 🇫🇷</option>
    </select>
  </div>
</nav>
"""

# Load model function
def load_model():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'crypto_liquidity_model.pkl')
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Streamlit page config
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# Show navbar
components.html(navbar_html, height=80, scrolling=False)

# Light-themed CSS with currency background pattern
st.markdown("""
<style>
body {
    padding-top: 80px;
    background-image: url('https://www.transparenttextures.com/patterns/cubes.png');
    background-color: #f9fafb;
    background-repeat: repeat;
    background-size: 60px 60px;
    color: #102a44;
    font-family: 'Poppins', Arial, sans-serif;
}

.stApp {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 12px;
    padding: 30px 40px 40px 40px;
    box-shadow: 0 8px 30px rgba(16, 42, 68, 0.15);
}

.title {
    text-align: center;
    color: #102a44 !important;
    font-size: 48px;
    font-weight: 700;
    margin-top: 15px;
}

.subtitle {
    text-align: center;
    color: #375a7f !important;
    font-size: 20px;
    margin-bottom: 20px;
}

.section {
    background-color: #f0f5fa;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 4px 10px rgba(16, 42, 68, 0.1);
    margin-top: 20px;
    color: #102a44 !important;
}

.disclaimer {
    background-color: #fff9e6;
    border-left: 6px solid #ffb347;
    padding: 15px;
    border-radius: 10px;
    margin-top: 30px;
    font-size: 14px;
    color: #463f0a;
}

.result-high {
    color: #388e3c;
    font-weight: bold;
}

.result-medium {
    color: #fbc02d;
    font-weight: bold;
}

.result-low {
    color: #d32f2f;
    font-weight: bold;
}

nav {
    background-color: #f5f7fa !important;
}

/* Inputs and buttons styling */
.stNumberInput>div>input {
    background-color: #fff !important;
    color: #102a44 !important;
    border: 1.5px solid #cdd9e5;
    border-radius: 6px;
    padding: 8px;
}

.stButton>button {
    background-color: #4ca1af;
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.stButton>button:hover {
    background-color: #397f86;
}

select {
    background-color: #fff;
    color: #102a44;
    font-weight: 600;
    padding: 5px;
    border-radius: 6px;
    border: 1.5px solid #cdd9e5;
}

a {
    color: #4ca1af;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Title & subtitle
st.markdown("<div class='title'>Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter crypto data to estimate <strong>Liquidity Level</strong>.</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
coin_names = sorted([
    'Bitcoin', 'Ethereum', 'Tether', 'BNB', 'XRP', 'Solana', 'Cardano',
    'Dogecoin', 'Shiba Inu', 'Polygon', 'Litecoin', 'Polkadot', 'Avalanche',
    'Uniswap', 'Chainlink', 'Stellar', 'VeChain', 'TRON', 'Filecoin', 'Near',
])

# Optional Coin Name input
selected_coin = st.selectbox(
    "Optional: Select a Coin Name",
    [""] + coin_names,  # Empty string allows for optional selection
    index=0,
    help="Start typing to select a coin from the list."
)

# Initialize session state variables
for key in ['open_price', 'high_price', 'low_price', 'close_price', 'volume']:
    if key not in st.session_state:
        st.session_state[key] = 0.0

# Demo data loader
def load_demo_data():
    st.session_state.open_price = 56787.5
    st.session_state.high_price = 64776.4
    st.session_state.low_price = 55000.0
    st.session_state.close_price = 63000.0
    st.session_state.volume = 123456.789

if st.button("Load Demo Data"):
    load_demo_data()

# Inputs in two columns
col1, col2 = st.columns(2)
with col1:
    open_price = st.number_input('Open Price', value=st.session_state.open_price, format="%.4f")
    high_price = st.number_input('High Price', value=st.session_state.high_price, format="%.4f")
    low_price = st.number_input('Low Price', value=st.session_state.low_price, format="%.4f")

    # Market Cap auto-calculation under low price
    market_cap = st.session_state.close_price * st.session_state.volume
    st.markdown(f"""
    <div style="margin-top: 10px; font-weight: bold; font-size: 16px; color:white;">
        Auto-calculated Market Cap:<br>
        <span style="color:#34e89e;">${market_cap:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    close_price = st.number_input('Close Price', value=st.session_state.close_price, format="%.4f")
    volume = st.number_input('Volume', value=st.session_state.volume, format="%.4f")

# Price overview chart
price_df = pd.DataFrame({
    "Price": [open_price, high_price, low_price, close_price]
}, index=["Open", "High", "Low", "Close"])
st.markdown("### Price Overview")
st.line_chart(price_df)

# Prepare input for model
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

# Load model
model = load_model()

# Classify liquidity
def classify_liquidity(score):
    if score < 0.4:
        return "<span class='result-low'>Low</span>"
    elif score < 0.7:
        return "<span class='result-medium'>Medium</span>"
    else:
        return "<span class='result-high'>High</span>"

# Predict trend
def predict_price_trend(open_p, close_p):
    if close_p > open_p:
        return "Price may go Up"
    elif close_p < open_p:
        return "Price may go Down"
    else:
        return "No Clear Price Movement"

# Disclaimer
st.markdown("""
<div class="disclaimer">
    <strong>Disclaimer:</strong><br>
    This tool uses an AI/ML model to make predictions based on input data.<br>
    Predictions are not guaranteed for any particular cryptocurrency or token.<br>
    No guarantees are made about accuracy or reliability. Use at your own risk.
</div>
""", unsafe_allow_html=True)

agree = st.checkbox("I acknowledge and accept the disclaimer above.")

# Predict button
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
