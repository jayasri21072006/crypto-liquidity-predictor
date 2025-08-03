import streamlit as st
import pickle
import json
import os

# ---------- CONFIG ----------
st.set_page_config(page_title="Crypto Predictor 🔮", page_icon="💧", layout="centered")

# ---------- UTILS ----------
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    else:
        return {}

# ---------- AUTH ----------
def register_user(email, password):
    users = load_users()
    if email in users:
        return False
    users[email] = password
    save_users(users)
    return True

def authenticate_user(email, password):
    users = load_users()
    return email in users and users[email] == password

# ---------- PAGES ----------
def show_login():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(email, password):
            st.session_state.logged_in = True
            st.session_state.email = email
            st.success("Login successful!")
        else:
            st.error("Invalid email or password.")

def show_register():
    st.title("📝 Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(email, password):
            st.success("Registered! You can now log in.")
        else:
            st.error("Email already exists. Try logging in.")

def show_prediction():
    st.title("🔮 Crypto Liquidity Predictor")
    model = load_model()

    st.markdown("### 📊 Enter values for prediction:")
    # Example input fields (customize as per your model)
    feature1 = st.number_input("Feature 1")
    feature2 = st.number_input("Feature 2")
    feature3 = st.number_input("Feature 3")

    if st.button("Predict"):
        features = [[feature1, feature2, feature3]]
        prediction = model.predict(features)
        st.success(f"🚀 Predicted Value: {prediction[0]}")

# ---------- MAIN ----------
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        choice = st.sidebar.radio("🔐 Auth Menu", ["Login", "Register"])
        if choice == "Login":
            show_login()
        else:
            show_register()
    else:
        show_prediction()

if __name__ == "__main__":
    main()

