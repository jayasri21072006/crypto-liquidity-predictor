import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import os
import base64

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Crypto Liquidity Predictor",
    page_icon="💧",
    layout="centered"
)

# --------------------------------------------------
# Background Image (LOCAL FILE)
# --------------------------------------------------
def set_bg_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        section[data-testid="stAppViewContainer"] {{
            background-color: rgba(255, 255, 255, 0.88);
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.15);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# image is inside streamlit_app/
set_bg_image("53540861975_5538e666cf_c.jpg")

# --------------------------------------------------
# Navbar
# --------------------------------------------------
navbar_html = """
<nav style="background-color:#102a44; color:white; display:flex; align-items:center;
padding:12px 30px; justify-content:space-between; border-radius:0 0 10px 10px;
box-shadow:0 4px 8px rgba(0,0,0,0.15);
font-family:Poppins, Arial; width:100vw; position:fixed; top:0; left:0; z-index:9999;">

  <div style="font-weight:700; font-size:26px;
  background:linear-gradient(90deg,#34e89e,#0f3443);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;">
  CryptoPredictions
  </div>

  <ul style="list-style:none; display:flex; gap:25px; margin:0;">
    <li><a href="https://cryptonews.com" target="_blank" style="color:white; text-decoration:none;">Market Updates</a></li>
    <li><a href="https://cryptopredictions.com/?results=200" target="_blank" style="color:white; text-decoration:none;">Coin List</a></li>
    <li><a href="https://cryptopredictions.com/blog/" target="_blank" style="color:white; text-decoration:none;">Insights</a></li>
  </ul>

  <div>
    <a href="https://twitter.com" target="_blank">
      <img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" width="22">
    </a>
    <a href="https://facebook.com" target="_blank">
      <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" width="22" style="margin-left:10px;">
    </a>
  </div>
</nav>
"""
components.html(navbar_html, height=80)

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>
body { padding-top:80px; font-family:Poppins, Arial; }
.title { text-align:center; font-size:48px; font-weight:800; color:#0044cc; }
.subtitle { text-align:center; font-size:20px; margin-bottom:25px; }
.result-high { color:#00c853; font-weight:bold; }
.result-medium { color:#ffb300; font-weight:bold; }
.result-low { color:#d50000; font-weight:bold; }
.disclaimer {
  background:#fff3cd;
  padding:15px;
  border-left:6px solid #ff9800;
  border-radius:10px;
  margin-top:25px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.markdown("<div class='title'>Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Estimate crypto <b>Liquidity Level</b> using ML</div>", unsafe_allow_html=True)
st.divider()

# --------------------------------------------------
# Model Loader
# --------------------------------------------------
def load_model():
    try:
        return joblib.load("crypto_liquidity_model.pkl")
    except Exception as e:
        st.error(f"Model load failed: {e}")
        return None

model = load_model()

# --------------------------------------------------
# Inputs
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    open_price = st.number_input("Open Price", value=56787.5)
    high_price = st.number_input("High Price", value=64776.4)
    low_price = st.number_input("Low Price", value=55000.0)

with col2:
    close_price = st.number_input("Close Price", value=63000.0)
    volume = st.number_input("Volume", value=123456.789)

# --------------------------------------------------
# Derived Features
# --------------------------------------------------
market_cap = close_price * volume
st.markdown(f"**Market Cap:** ${market_cap:,.2f}")

price_df = pd.DataFrame(
    {"Price": [open_price, high_price, low_price, close_price]},
    index=["Open", "High", "Low", "Close"]
)
st.line_chart(price_df)

# --------------------------------------------------
# Prediction Input
# --------------------------------------------------
input_data = pd.DataFrame({
    "Open": [open_price],
    "High": [high_price],
    "Low": [low_price],
    "Close": [close_price],
    "Volume": [volume],
    "Market Cap": [market_cap],
    "SMA_5": [0],
    "EMA_12": [0],
    "RSI": [0],
    "MACD": [0],
})

def classify(score):
    if score < 0.4:
        return "<span class='result-low'>Low</span>"
    elif score < 0.7:
        return "<span class='result-medium'>Medium</span>"
    return "<span class='result-high'>High</span>"

def trend(o, c):
    if c > o: return "Price may go UP 📈"
    if c < o: return "Price may go DOWN 📉"
    return "Sideways movement"

# --------------------------------------------------
# Disclaimer
# --------------------------------------------------
st.markdown("""
<div class="disclaimer">
<b>Disclaimer:</b><br>
This prediction is ML-based and not financial advice.
Crypto markets are volatile. Use responsibly.
</div>
""", unsafe_allow_html=True)

agree = st.checkbox("I understand and accept the disclaimer")

# --------------------------------------------------
# Predict
# --------------------------------------------------
if st.button("🔮 Predict Liquidity"):
    if not agree:
        st.warning("Please accept the disclaimer.")
    elif model is None:
        st.error("Model not available.")
    else:
        score = model.predict(input_data)[0]
        st.markdown(f"""
        <h3 style="text-align:center;">Prediction Result</h3>
        <p><b>Liquidity Score:</b> {score:.2f}</p>
        <p><b>Liquidity Level:</b> {classify(score)}</p>
        <p><b>Trend:</b> {trend(open_price, close_price)}</p>
        """, unsafe_allow_html=True)
