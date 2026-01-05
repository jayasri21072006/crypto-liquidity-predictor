import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import os
import base64

# ------------------ NAVBAR ------------------
navbar_html = """
<nav style="background-color:#102a44; color:white; display:flex; align-items:center;
padding:12px 30px; justify-content:space-between; border-radius:0 0 10px 10px;
box-shadow:0 4px 8px rgba(0,0,0,0.1); font-family:'Poppins', Arial, sans-serif;
width:100vw; position:fixed; top:0; left:0; z-index:9999; box-sizing:border-box;">
  <div style="font-weight:700; font-size:26px;
  background:linear-gradient(90deg,#34e89e,#0f3443);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
    CryptoPredictions
  </div>
</nav>
"""

# ------------------ LOAD BACKGROUND IMAGE LOCALLY ------------------
def load_bg_image():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "53540861975_5538e666cf_c.jpg")

    with open(img_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    return f"data:image/jpg;base64,{data}"

# ------------------ MODEL LOADER ------------------
def load_model():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'crypto_liquidity_model.pkl')
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")
components.html(navbar_html, height=80)

# ------------------ CSS ------------------
st.markdown("""
<style>
.background-watermark {
    position: fixed;
    top: 55%;
    left: 50%;
    width: 260px;
    opacity: 0.12;
    transform: translate(-50%, -50%);
    z-index: -1;
}
.title {text-align:center; font-size:50px; font-weight:bold; color:#0044cc;}
.subtitle {text-align:center; font-size:20px;}
.stApp {padding-top:90px;}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<div class='title'>Crypto Liquidity Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter crypto data to estimate Liquidity Level</div><hr>", unsafe_allow_html=True)

# ------------------ BACKGROUND IMAGE ------------------
bg_img = load_bg_image()
st.markdown(f"<img class='background-watermark' src='{bg_img}'>", unsafe_allow_html=True)

# ------------------ INPUTS ------------------
open_price = st.number_input("Open Price", 0.0)
high_price = st.number_input("High Price", 0.0)
low_price = st.number_input("Low Price", 0.0)
close_price = st.number_input("Close Price", 0.0)
volume = st.number_input("Volume", 0.0)

market_cap = close_price * volume
st.write("Market Cap:", market_cap)

price_df = pd.DataFrame({"Price":[open_price, high_price, low_price, close_price]},
                        index=["Open","High","Low","Close"])
st.line_chart(price_df)

# ------------------ MODEL INPUT ------------------
input_data = pd.DataFrame({
    'Open':[open_price],
    'High':[high_price],
    'Low':[low_price],
    'Close':[close_price],
    'Volume':[volume],
    'Market Cap':[market_cap],
    'SMA_5':[0],
    'EMA_12':[0],
    'RSI':[0],
    'MACD':[0]
})

model = load_model()

# ------------------ PREDICT ------------------
if st.button("Predict Liquidity"):
    if model:
        score = model.predict(input_data)[0]
        st.success(f"Liquidity Score: {score:.2f}")
    else:
        st.error("Model file not found.")
