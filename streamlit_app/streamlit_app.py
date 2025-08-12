import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import os

# --- Updated Navbar HTML with fixed position and full width ---
navbar_html = """
<nav style="
  background-color:#102a44; 
  color:white; 
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
    <div style="font-weight:700; font-size:26px; background: linear-gradient(90deg, #34e89e, #0f3443); -webkit-background-clip: text; -webkit-text-fill-color: transparent; user-select:none; cursor:default;">CryptoPredictions</div>
  </div>

  <ul style="list-style:none; display:flex; margin:0; padding:0;">
    <li style="margin: 0 20px;"><a href="https://cryptonews.com" target="_blank" style="color:white; text-decoration:none; font-weight:600; font-size:16px;">Market Updates</a></li>
    <li style="margin: 0 20px;"><a href="https://cryptopredictions.com/?results=200" target="_blank" style="color:white; text-decoration:none; font-weight:600; font-size:16px;">Coin List</a></li>
    <li style="margin: 0 20px;"><a href="https://cryptopredictions.com/blog/" target="_blank" style="color:white; text-decoration:none; font-weight:600; font-size:16px;">Insights Blog</a></li>
  </ul>

  <div style="display:flex; align-items:center; gap:20px;">
    <div>
      <a href="https://twitter.com" target="_blank" aria-label="Twitter"><img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="Twitter" style="width:24px; height:24px; cursor:pointer; filter:brightness(100%); transition:filter 0.3s ease;"></a>
      <a href="https://facebook.com" target="_blank" aria-label="Facebook"><img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook" style="width:24px; height:24px; cursor:pointer; filter:brightness(100%); transition:filter 0.3s ease; margin-left: 10px;"></a>
    </div>
    <select aria-label="Select Language" style="background:transparent; border:none; color:white; font-weight:600; font-size:15px; cursor:pointer; padding:4px; border-radius:4px; transition:background-color 0.3s ease;">
      <option value="en" selected>English 🇬🇧</option>
      <option value="es">Español 🇪🇸</option>
      <option value="fr">Français 🇫🇷</option>
    </select>
  </div>
</nav>
"""

# Load ML Model safely
def load_model():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'crypto_liquidity_model.pkl')
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Page setup
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

# Show navbar
components.html(navbar_html, height=80, scrolling=False)

# Add padding to body to prevent overlap with fixed navbar
st.markdown("""
<style>
body {
    padding-top: 80px;
}
.title {
    text-align: center;
    color: #0044cc;
    font-size: 50px;
    font-weight: bold;
    margin-top: 15px;
}
.subtitle {
    text-align: center;
    color: #333;
    font-size: 20px;
    margin-bottom: 20px;
}
.section {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
    margin-top: 20px;
}
.disclaimer {
    background-color: #fff4e6;
    border-left: 6px solid #ff9800;
    padding: 15px;
    border-radius: 10px;
    margin-top: 30px;
    font-size: 18px;
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
</style>
""", unsafe_allow_html=True)

# Title & subtitle
st.markdown("<div class='title'>Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter crypto data to estimate <strong>Liquidity Level</strong>.</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

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
    open_price = st.number_input('Open Price', value=st.session_state.open_price, format="%.4f",
                                help="Price at which crypto opened during trading period.")
    high_price = st.number_input('High Price', value=st.session_state.high_price, format="%.4f",
                                help="Highest price crypto reached during trading period.")
    low_price = st.number_input('Low Price', value=st.session_state.low_price, format="%.4f",
                               help="Lowest price crypto reached during trading period.")

    # Market Cap auto-calculation under low price
    market_cap = st.session_state.close_price * st.session_state.volume
    st.markdown(f"""
    <div style="margin-top: 10px; font-weight: bold; font-size: 16px;">
        Auto-calculated Market Cap:<br>
        <span style="color:#0044cc;">${market_cap:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    close_price = st.number_input('Close Price', value=st.session_state.close_price, format="%.4f",
                                 help="Price at which crypto closed during trading period.")
    volume = st.number_input('Volume', value=st.session_state.volume, format="%.4f",
                            help="Total amount of crypto traded during trading period.")

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

# Liquidity classifier
def classify_liquidity(score):
    if score < 0.4:
        return "<span class='result-low'>Low</span>"
    elif score < 0.7:
        return "<span class='result-medium'>Medium</span>"
    else:
        return "<span class='result-high'>High</span>"

# Price trend prediction
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
    No guarantees are made about accuracy or reliability. Use at your own risk.
</div>
""", unsafe_allow_html=True)

agree = st.checkbox("I acknowledge and accept the disclaimer above.")

# Prediction button
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
                <p><strong>Liquidity Score:</strong> {score:.2f}</p>
                <p><strong>Liquidity Level:</strong> {liquidity_level}</p>
                <p><strong>Price Trend:</strong> {trend}</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
    else:
        st.warning("Please accept the disclaimer to proceed.")

