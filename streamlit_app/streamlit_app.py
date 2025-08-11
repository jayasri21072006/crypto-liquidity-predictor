import streamlit as st

# ---------------------- CUSTOM CSS ----------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* 🌍 Crypto Currency Background */
    body {
        background-image: url('https://images.unsplash.com/photo-1620317586356-3d9c8e9d3a17'); /* Replace with your image URL */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Overlay for readability */
    .main {
        background-color: rgba(255, 255, 255, 0.88);
        border-radius: 15px;
        padding: 20px;
    }

    /* Title Styling */
    .title {
        text-align: center;
        font-size: 65px;
        font-weight: 900;
        background: linear-gradient(90deg, #ff6f61, #ff9800, #ffca28);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
        margin-top: 20px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        color: #4a148c;
        margin-bottom: 25px;
    }

    /* Input Labels */
    .stNumberInput label {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #d84315 !important;
    }

    /* Input Boxes */
    .stNumberInput input {
        font-size: 18px !important;
        height: 45px !important;
        border-radius: 8px !important;
    }

    /* Predict Button */
    div.stButton > button:first-child {
        font-size: 20px;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 700;
        background: linear-gradient(90deg, #ff6f61, #ff9800);
        color: white;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05);
        box-shadow: 0px 4px 15px rgba(255, 152, 0, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- APP CONTENT ----------------------
st.markdown("<h1 class='title'>💹 Crypto Liquidity Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Enter key crypto data to estimate Liquidity Level.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    open_price = st.number_input("🔓 Open Price", min_value=0.0, format="%.4f")
    high_price = st.number_input("🔼 High Price", min_value=0.0, format="%.4f")
    low_price = st.number_input("🔽 Low Price", min_value=0.0, format="%.4f")

with col2:
    close_price = st.number_input("🔒 Close Price", min_value=0.0, format="%.4f")
    volume = st.number_input("📊 Volume", min_value=0.0, format="%.4f")

# Auto-calculated market cap (example logic)
market_cap = (open_price + close_price) / 2 * volume
st.info(f"💰 Auto-Calculated Market Cap: {market_cap:,.2f}")

# Disclaimer
st.warning("⚠ Disclaimer: This tool uses an AI/ML model to make predictions based on input data. "
           "We do not guarantee accuracy, and we are not responsible for any financial losses.")

# Checkbox for acceptance
accept = st.checkbox("✅ I acknowledge and accept the disclaimer above.")

# Predict Button
if st.button("🔮 Predict Liquidity") and accept:
    # Placeholder for prediction logic
    st.success("📈 Predicted Liquidity Level: High")
elif st.button("🔮 Predict Liquidity"):
    st.error("Please accept the disclaimer before predicting.")

