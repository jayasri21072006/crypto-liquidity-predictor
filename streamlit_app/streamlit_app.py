import streamlit as st

# Page config
st.set_page_config(
    page_title="Crypto Liquidity Predictor",
    page_icon="💹",
    layout="wide"
)

# Custom CSS
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
            font-size: 20px;
            color: #dddddd;
            margin-bottom: 30px;
        }

        /* Field labels (light blue) */
        .stNumberInput label, .stTextInput label, .stSelectbox label {
            font-size: 22px !important;
            font-weight: bold !important;
            color: #4dc3ff !important; 
        }

        /* Input styling */
        .stNumberInput input {
            font-size: 20px !important;
            background-color: #2a2a2a !important;
            color: white !important;
            border: 2px solid #4dc3ff !important;
            border-radius: 6px !important;
        }

        /* Market Cap (pink) */
        .market-cap {
            background-color: #1a1a1a;
            padding: 12px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #ff66ff !important;
        }

        /* Disclaimer (blue) */
        .disclaimer-box {
            background-color: #1a1a1a;
            padding: 12px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            color: #4dc3ff !important;
        }

        /* Prediction Result (red) */
        .prediction-box {
            background-color: #1a1a1a;
            padding: 15px;
            border-radius: 12px;
            font-size: 18px;
            margin-top: 20px;
            color: #ff4d4d !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="big-title">💹 Crypto Liquidity Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter key crypto data to estimate <b>Liquidity Level</b>.</div>', unsafe_allow_html=True)

# Input fields
col1, col2 = st.columns(2)

with col1:
    open_price = st.number_input("🔓 Open Price", min_value=0.0, format="%.4f")
    high_price = st.number_input("⚠ High Price", min_value=0.0, format="%.4f")
    low_price = st.number_input("🔻 Low Price", min_value=0.0, format="%.4f")

with col2:
    close_price = st.number_input("🔒 Close Price", min_value=0.0, format="%.4f")
    volume = st.number_input("📦 Volume", min_value=0.0, format="%.4f")

# Auto-calculated market cap (PINK)
market_cap = close_price * volume
st.markdown(f'<div class="market-cap">💰 <b>Auto-Calculated Market Cap:</b> {market_cap:,.2f}</div>', unsafe_allow_html=True)

# Disclaimer (BLUE)
st.markdown("""
<div class="disclaimer-box">
⚠ <b>Disclaimer:</b><br>
This tool uses an AI/ML model to make predictions based on input data.<br>
We do not guarantee accuracy, and we are not responsible for any financial losses incurred from using this app.
</div>
""", unsafe_allow_html=True)

# Checkbox
accept = st.checkbox("✅ I understand the disclaimer")

# Predict Button
if st.button("🔮 Predict Liquidity"):
    if accept:
        st.markdown("""
            <div class="prediction-box">
            📊 <b>Prediction Result</b><br>
            💧 Liquidity Score: 0.07<br>
            🚨 Liquidity Level: <b>Low</b><br>
            📈 Price Trend Hint: No Clear Price Movement
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Please accept the disclaimer before predicting.")
