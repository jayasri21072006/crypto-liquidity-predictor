import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import os
import base64

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

# --- Background Image (Base64) ---
def get_base64_of_bin(file_path):
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def set_background(image_path):
    bin_str = get_base64_of_bin(image_path)
    css = f"""
    <style>
    body {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .stApp {{
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- Load ML Model ---
def load_model():
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        return None

# --- Streamlit App Setup ---
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")
components.html(navbar_html, height=80, scrolling=False)

# Adjust the path for your background image here:
set_background(os.path.join(os.path.dirname(__file__), "Screenshot (96).png"))

# --- Title & Subtitle ---
st.markdown("<h1 style='color:white;'>Crypto Liquidity Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:white;'>Enter crypto data to estimate <strong>Liquidity Level</strong>.</p><hr>", unsafe_allow_html=True)

# --- Coin Selection ---
coin_names = sorted([
    'Bitcoin', 'Ethereum', 'Tether', 'BNB', 'XRP', 'Solana', 'Cardano',
    'Dogecoin', 'Shiba Inu', 'Polygon', 'Litecoin', 'Polkadot', 'Avalanche',
    'Uniswap', 'Chainlink', 'Stellar', 'VeChain', 'TRON', 'Filecoin', 'Near',
])
selected_coin = st.selectbox("Optional: Select a Coin", [""] + coin_names)

# --- Default Inputs ---
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

# --- Input Fields ---
col1, col2 = st.columns(2)
with col1:
    open_price = st.number_input('Open Price', value=st.session_state.open_price, format="%.4f")
    high_price = st.number_input('High Price', value=st.session_state.high_price, format="%.4f")
    low_price = st.number_input('Low Price', value=st.session_state.low_price, format="%.4f")
with col2:
    close_price = st.number_input('Close Price', value=st.session_state.close_price, format="%.4f")
    volume = st.number_input('Volume', value=st.session_state.volume, format="%.4f")

# --- Update session state ---
st.session_state.open_price = open_price
st.session_state.high_price = high_price
st.session_state.low_price = low_price
st.session_state.close_price = close_price
st.session_state.volume = volume

# --- Market Cap Calculation ---
market_cap = close_price * volume
st.markdown(f"<h4 style='color:#00c8ff;'>Market Cap: ${market_cap:,.2f}</h4>", unsafe_allow_html=True)

# --- Price Line Chart ---
price_df = pd.DataFrame({
    "Price": [open_price, high_price, low_price, close_price]
}, index=["Open", "High", "Low", "Close"])
st.line_chart(price_df)

# --- Model Input Data ---
input_data = pd.DataFrame({
    'Open': [open_price],
    'High': [high_price],
    'Low': [low_price],
    'Close': [close_price],
    'Volume': [volume],
    'Market Cap': [market_cap],
    # Placeholder for additional features:
    'SMA_5': [0],
    'EMA_12': [0],
    'RSI': [0],
    'MACD': [0]
})

# --- Load the model ---
model = load_model()

# --- Classification Helper ---
def classify_liquidity(score):
    if score < 0.4:
        return "<span style='color:red; font-weight:bold;'>Low</span>"
    elif score < 0.7:
        return "<span style='color:yellow; font-weight:bold;'>Medium</span>"
    else:
        return "<span style='color:lightgreen; font-weight:bold;'>High</span>"

def predict_trend(open_p, close_p):
    if close_p > open_p:
        return "📈 Price likely to increase"
    elif close_p < open_p:
        return "📉 Price likely to decrease"
    else:
        return "⚖️ No significant movement"

# --- Disclaimer ---
st.markdown("""
<div style="background-color: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px;">
<b>Disclaimer:</b><br>
This is an AI-based tool and predictions are for informational purposes only. Use at your own risk.
</div>
""", unsafe_allow_html=True)
agree = st.checkbox("I agree to the disclaimer above.")

# --- Prediction Button ---
if st.button("Predict Liquidity"):
    if not model:
        st.error("Model not loaded.")
    elif not agree:
        st.warning("You must accept the disclaimer to proceed.")
    else:
        try:
            score = model.predict(input_data)[0]
            liquidity = classify_liquidity(score)
            trend = predict_trend(open_price, close_price)

            st.markdown(f"""
            <div style='text-align:center;'>
                <h3>Prediction Results</h3>
                <p><strong>Liquidity Level:</strong> {liquidity}</p>
                <p><strong>Trend:</strong> {trend}</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
