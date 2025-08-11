import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Crypto Liquidity Predictor", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
            color: white;
        }

        /* Title style */
        .main-title {
            font-size: 60px;
            font-weight: bold;
            color: #ff66cc;
            text-align: center;
            text-shadow: 0px 0px 20px #ff66cc;
        }

        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 20px;
            margin-bottom: 20px;
        }

        /* Increase input label size */
        label {
            font-size: 18px !important;
            font-weight: 600 !important;
            color: #ffffff !important;
        }

        /* Card style for calculated market cap */
        .stMetric {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 10px;
        }

        /* Disclaimer box */
        .disclaimer {
            background-color: rgba(255, 204, 0, 0.2);
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="main-title">💱 Crypto Liquidity Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter key crypto data to estimate <b>Liquidity Level</b>.</div>', unsafe_allow_html=True)

# --- Input fields ---
col1, col2 = st.columns(2)

with col1:
    open_price = st.number_input("🔓 Open Price", min_value=0.0, format="%.4f")
    high_price = st.number_input("🔺 High Price", min_value=0.0, format="%.4f")
    low_price = st.number_input("🔻 Low Price", min_value=0.0, format="%.4f")

with col2:
    close_price = st.number_input("🔒 Close Price", min_value=0.0, format="%.4f")
    volume = st.number_input("📦 Volume", min_value=0.0, format="%.4f")

# --- Auto-calculated Market Cap ---
market_cap = close_price * volume
st.markdown(f"**💰 Auto-Calculated Market Cap:** <span style='color:#00ff99;'>{market_cap:,.2f}</span>", unsafe_allow_html=True)

# --- Disclaimer ---
st.markdown("""
<div class="disclaimer">
⚠ <b>Disclaimer:</b>  
This tool uses an AI/ML model to make predictions based on input data.  
We do not guarantee accuracy, and we are not responsible for any financial losses incurred from using this app.
</div>
""", unsafe_allow_html=True)

# --- Predict Button ---
accept = st.checkbox("I accept the disclaimer above.")
predict_clicked = st.button("🔮 Predict Liquidity")

if predict_clicked:
    if accept:
        st.success("📈 Predicted Liquidity Level: High")
    else:
        st.error("Please accept the disclaimer before predicting.")


