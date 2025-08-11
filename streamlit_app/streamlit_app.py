import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💹", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
        /* Background */
        body, .stApp {
            background-color: #2e2e2e !important;
            color: white !important;
        }

        /* Big Neon Title */
        .big-title {
            font-size: 55px;
            text-align: center;
            color: #ff66ff;
            font-weight: bold;
            text-shadow: 0px 0px 25px #ff66ff;
        }

        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 38px !important;
            font-weight: bold !important;
            color: #00bfff !important;
            text-shadow: 0px 0px 8px #00bfff;
            margin-bottom: 30px;
        }

        /* Field labels */
        .stNumberInput label, .stTextInput label, .stSelectbox label {
            font-size: 38px !important;  
            font-weight: bold !important;
            color: #00bfff !important; 
            text-shadow: 0px 0px 8px #00bfff;
        }

        /* Input styling */
        .stNumberInput input {
            font-size: 24px !important;
            background-color: #2a2a2a !important;
            color: white !important;
            border: 2px solid #00bfff !important;
            border-radius: 6px !important;
        }

        /* Market Cap (pink) */
        .market-cap {
            background-color: #1a1a1a;
            padding: 12px;
            border-radius: 10px;
            font-size: 20px;
            font-weight: bold;
            color: #ff66ff !important;
        }

        /* Disclaimer (blue) */
        .disclaimer-box {
            background-color: #1a1a1a;
            padding: 12px;
            border-radius: 10px;
            font-size: 20px;
            font-weight: bold;
            color: #4dc3ff !important;
        }

        /* EVERYTHING below disclaimer in pink */
        .below-disclaimer {
            color: #ff66ff !important;
            font-weight: bold;
        }

        /* Prediction Result (pink) */
        .prediction-box {
            background-color: #1a1a1a;
            padding: 15px;
            border-radius: 12px;
            font-size: 20px;
            margin-top: 20px;
            color: #ff66ff !important;
        }

        /* Pink button text */
        div.stButton > button {
            background-color: #1a1a1a !important;
            color: #ff66ff !important;
            font-size: 20px !important;
            font-weight: bold;
            border: 2px solid #ff66ff !important;
            border-radius: 8px;
        }
        div.stButton > button:hover {
            background-color: #ff66ff !important;
            color: black !important;
        }

        /* Checkbox label in large orange without blur */
        div[data-testid="stCheckbox"] label {
            color: orange !important;
            font-size: 38px !important;
            font-weight: bold !important;
            text-shadow: 0px 0px 6px orange;
            opacity: 1 !important; /* remove Streamlit fade */
        }
    </style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="big-title">💹 Crypto Liquidity Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter key crypto data to estimate <b>Liquidity Level</b>.</div>', unsafe_allow_html=True)

# ---------- INPUTS ----------
col1, col2 = st.columns(2)

with col1:
    open_price = st.number_input("🔓 Open Price", value=0.0000, format="%.4f")
    high_price = st.number_input("⚠ High Price", value=0.0000, format="%.4f")
    low_price = st.number_input("🔻 Low Price", value=0.0000, format="%.4f")

with col2:
    close_price = st.number_input("🔒 Close Price", value=0.0000, format="%.4f")
    volume = st.number_input("📦 Volume", value=0.0000, format="%.4f")

# Auto Calculate Market Cap
market_cap = close_price * volume
st.markdown(f'<div class="market-cap">💰 Auto-Calculated Market Cap: {market_cap:.2f}</div>', unsafe_allow_html=True)

# Disclaimer
st.markdown('<div class="disclaimer-box">⚠ Disclaimer: This tool uses an AI/ML model to make predictions based on input data. We do not guarantee accuracy, and we are not responsible for any financial losses incurred from using this app.</div>', unsafe_allow_html=True)

# BELOW DISCLAIMER CONTENT
st.markdown('<div class="below-disclaimer">', unsafe_allow_html=True)

agree = st.checkbox("✅ I understand the disclaimer")
if agree:
    if st.button("🔮 Predict Liquidity Level"):
        # Simple placeholder prediction logic
        if market_cap > 1000000:
            prediction = "High Liquidity"
        elif market_cap > 500000:
            prediction = "Medium Liquidity"
        else:
            prediction = "Low Liquidity"

        st.markdown(f'<div class="prediction-box">📊 Prediction: {prediction}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


