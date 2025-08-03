import streamlit as st
import joblib
import pandas as pd
import os

# -------- User "Database" (in-memory for now) --------
if "user_db" not in st.session_state:
    st.session_state.user_db = {"admin": "1234"}

# -------- Session state --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# -------- Register --------
def register():
    st.subheader("📝 Register New Account")
    new_user = st.text_input("Choose Username (Email)")
    new_pass = st.text_input("Create Password", type="password")
    if st.button("Register"):
        if new_user in st.session_state.user_db:
            st.warning("⚠️ User already exists.")
        else:
            st.session_state.user_db[new_user] = new_pass
            st.success("✅ Registered! You can now log in.")

# -------- Login --------
def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in st.session_state.user_db and st.session_state.user_db[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Welcome, {username}!")
        else:
            st.error("❌ Invalid credentials")

# -------- Main App After Login --------
def run_app():
    st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")

    st.markdown("""
        <h1 style='text-align: center; color: #00BFFF;'>🪙 Crypto Liquidity Predictor</h1>
        <p style='text-align: center;'>Enter key crypto data to estimate <strong>Liquidity Level</strong>.</p>
        <hr>
    """, unsafe_allow_html=True)

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        open_price = st.number_input('🔓 Open Price', value=0.0)
        high_price = st.number_input('🔺 High Price', value=0.0)
        low_price = st.number_input('🔻 Low Price', value=0.0)
    with col2:
        close_price = st.number_input('🔒 Close Price', value=0.0)
        volume = st.number_input('📦 Volume', value=0.0)
        market_cap = st.number_input('💰 Market Cap', value=0.0)

    input_data = pd.DataFrame({
        'Open': [open_price],
        'High': [high_price],
        'Low': [low_price],
        'Close': [close_price],
        'Volume': [volume],
        'Market Cap': [market_cap],
        'SMA_5': [0],
        'EMA_12': [0],
        'RSI': [0],
        'MACD': [0]
    })

    def classify_liquidity(score):
        if score < 0.4:
            return "🟥 Low"
        elif score < 0.7:
            return "🟨 Medium"
        else:
            return "🟩 High"

    def predict_price_trend(open_price, close_price):
        if close_price > open_price:
            return "📈 Price may go Up"
        elif close_price < open_price:
            return "📉 Price may go Down"
        else:
            return "❓ No Clear Price Movement"

    if st.button("🔍 Predict Liquidity"):
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
            model = joblib.load(model_path)
            score = model.predict(input_data)[0]
            liquidity_level = classify_liquidity(score)
            trend = predict_price_trend(open_price, close_price)

            st.markdown(f"""
            ### 📊 Prediction Result

            - 💧 **Liquidity Score**: {score:.2f}  
            - 🔵 **Liquidity Level**: {liquidity_level}  
            - 📉 **Price Trend Hint**: {trend}  
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

    # Logout button
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# -------- Main Layout --------
def main():
    st.sidebar.title("🔐 Auth Menu")
    menu = ["Login", "Register"]
    choice = st.sidebar.radio("Select Option", menu)

    if not st.session_state.logged_in:
        if choice == "Login":
            login()
        else:
            register()
    else:
        run_app()

# -------- Run --------
if __name__ == "__main__":
    main()
