import streamlit as st

# Page config
st.set_page_config(
    page_title="Crypto Liquidity Predictor",
    page_icon="💹",
    layout="wide"
)

# Custom CSS for better visibility in dark mode
st.markdown("""
    <style>
        /* Background */
        body, .stApp {
            background-color: #1e1e1e !important;
            color: white !important;
        }

        /* Big Neon Title */
        .big-title {
            font-size: 60px;
            text-align: center;
            color: #ff66ff;
            font-weight: bold;
            text-shadow: 0px 0px 25px #ff66ff;
        }

        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 22px;
            color: #eeeeee;
            margin-bottom: 30px;
        }

        /* Bigger input labels */
        label {
            font-size: 24px !important;
            font-weight: bold !important;
            color: #ffffff !important;
        }

        /* Input fields */
        .stNumberInput input {
            font-size: 20px !important;
            background-color: #333333 !important;
            color: white !important;
            border: 2px solid #666666 !important;
            border-radius: 8px !important;
        }

        /* Market Cap Box */
        .market-cap {
            background-color: #2b2b2b;
            padding: 12px;
            border-radius: 10px;
            font-size: 20px;
            color: white;
        }

        /* Warning box style */
        .stAlert {
            background-color: #4a3f00 !important;
            color: #ffcc00 !important;
            font-size: 18px;
            border-radius: 8px;
        }

        /* Prediction Result Box */
        .prediction-box {
            background-color: #2b2b2b;
            padding: 15px;
            border-radius: 12px;
            font-size: 20px;
            color: white;
            margin-top: 20px;
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

# Auto-calculated market cap
market_cap = close_price * volume
st.markdown(
    f'<div class="market-cap">💰 <b>Auto-Calculated Market Cap:</b> '
    f'<span style="color: lightgreen;">{market_cap:,.2f}</span></div>',
    unsafe_allow_html=True
)

# Disclaimer
st.warning("""
⚠ **Disclaimer**:  
This tool uses an AI/ML model to make predictions based on input data.  
We do not guarantee accuracy, and we are not responsible for any financial losses incurred from using this app.
""")

# Prediction button
accept = st.checkbox("✅ I understand the disclaimer")

if st.button("🔮 Predict Liquidity"):
    if accept:
        st.markdown("""
            <div class="prediction-box">
            📊 **Prediction Result**  
            💧 Liquidity Score: 0.07  
            🚨 Liquidity Level: **Low**  
            📈 Price Trend Hint: No Clear Price Movement
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Please accept the disclaimer before predicting.")



