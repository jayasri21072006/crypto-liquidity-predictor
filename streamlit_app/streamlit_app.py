import streamlit as st

# Set page config (Dark Theme default)
st.set_page_config(
    page_title="Crypto Liquidity Predictor",
    page_icon="💹",
    layout="wide"
)

# Inject custom CSS for dark theme and label size increase
st.markdown("""
    <style>
        /* Dark background */
        body, .stApp {
            background-color: #2e2e2e !important;
            color: white !important;
        }

        /* Header Styling */
        .big-title {
            font-size: 50px;
            text-align: center;
            color: #ff66ff;
            font-weight: bold;
            text-shadow: 0px 0px 20px #ff66ff;
        }

        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #dddddd;
            margin-bottom: 30px;
        }

        /* Bigger form labels */
        label {
            font-size: 18px !important;
            font-weight: 600 !important;
            color: white !important;
        }

        /* Market Cap Box */
        .market-cap {
            background-color: #1a1a1a;
            padding: 10px;
            border-radius: 10px;
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
st.markdown(f'<div class="market-cap">💰 <b>Auto-Calculated Market Cap:</b> <span style="color: lightgreen;">{market_cap:,.2f}</span></div>', unsafe_allow_html=True)

# Disclaimer
st.warning("""
⚠ **Disclaimer**:  
This tool uses an AI/ML model to make predictions based on input data.  
We do not guarantee accuracy, and we are not responsible for any financial losses incurred from using this app.
""")

# Prediction button
accept = st.checkbox("✅ I understand the disclaimer")

predict_clicked = st.button("🔮 Predict Liquidity")
if predict_clicked:
    if accept:
        st.success("📈 Predicted Liquidity Level: High")
    else:
        st.error("Please accept the disclaimer before predicting.")


