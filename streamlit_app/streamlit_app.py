import streamlit as st

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Crypto Liquidity Predictor", layout="wide")

# ---- CSS STYLING ----
st.markdown("""
    <style>
    /* Background color */
    .stApp {
        background-color: #2e2e2e;  /* mild dark gray */
        background-size: cover;
    }

    /* Header */
    .big-header {
        font-size: 50px !important;
        font-weight: bold;
        color: #ff66ff;
        text-shadow: 0px 0px 10px #ff99ff;
        text-align: center;
    }

    /* Subtitle same size as labels */
    .subtitle {
        font-size: 26px !important;
        font-weight: bold;
        color: #00ccff;
        text-align: center;
    }

    /* Input labels - bigger font */
    label {
        font-size: 22px !important;
        font-weight: bold;
        color: #00ccff !important;
    }

    /* Open Price bigger & bright blue */
    label[for="🔓 Open Price"] {
        color: #0099ff !important;
        font-size: 28px !important;
        font-weight: bold !important;
    }

    /* Market Cap pink */
    .market-cap {
        color: #ff00aa !important;
        font-weight: bold;
        font-size: 20px !important;
    }

    /* Disclaimer text */
    .disclaimer {
        color: #00ccff !important;
        font-size: 16px !important;
    }

    /* All below disclaimer in pink */
    .below-disc {
        color: #ff66ff !important;
        font-size: 18px !important;
        font-weight: bold;
        text-shadow: 0px 0px 6px #ff66ff;
    }

    /* Checkbox label pink + glow */
    div.stCheckbox label {
        color: #ff66ff !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-shadow: 0px 0px 6px #ff66ff;
    }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown('<div class="big-header">💹 Crypto Liquidity Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter key crypto data to estimate Liquidity Level.</div>', unsafe_allow_html=True)

# ---- INPUT FIELDS ----
col1, col2 = st.columns(2)

with col1:
    open_price = st.number_input("🔓 Open Price", format="%.4f")
    high_price = st.number_input("⚠ High Price", format="%.4f")
    low_price = st.number_input("🔻 Low Price", format="%.4f")

with col2:
    close_price = st.number_input("🔒 Close Price", format="%.4f")
    volume = st.number_input("📊 Volume", format="%.4f")

# ---- MARKET CAP DISPLAY ----
market_cap = (open_price + close_price) / 2 * volume
st.markdown(f'<p class="market-cap">💰 Auto-Calculated Market Cap: {market_cap:.2f}</p>', unsafe_allow_html=True)

# ---- DISCLAIMER ----
st.markdown('<p class="disclaimer">⚠ Disclaimer: This tool uses an AI/ML model to make predictions based on input data. '
            'We do not guarantee accuracy, and we are not responsible for any financial losses incurred from using this app.</p>',
            unsafe_allow_html=True)

# ---- BELOW DISCLAIMER TEXT ----
agree = st.checkbox("I understand the disclaimer")
if agree:
    st.markdown('<p class="below-disc">✔ You acknowledged the disclaimer. Proceed with caution!</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="below-disc">❗ You must agree to the disclaimer before using the app.</p>', unsafe_allow_html=True)

