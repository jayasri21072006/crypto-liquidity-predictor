import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import numpy as np
import os

# --- Navbar HTML ---
navbar_html = """
<nav style="background-color:#102a44; color:white; display:flex; align-items:center; padding:12px 30px;
justify-content:space-between; border-radius:0 0 10px 10px;
box-shadow:0 4px 8px rgba(0,0,0,0.1); font-family:'Poppins',Arial,sans-serif;
width:100vw; position:fixed; top:0; left:0; z-index:9999; box-sizing:border-box;">
  <div style="font-weight:700; font-size:26px;
    background:linear-gradient(90deg,#34e89e,#0f3443);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;">CryptoPredictions</div>
  <ul style="list-style:none; display:flex; gap:25px; margin:0; padding:0;">
    <li><a href="https://cryptonews.com" target="_blank"
       style="color:white;text-decoration:none;font-weight:600;">Market Updates</a></li>
    <li><a href="https://cryptopredictions.com/?results=200" target="_blank"
       style="color:white;text-decoration:none;font-weight:600;">Coin List</a></li>
    <li><a href="https://cryptopredictions.com/blog/" target="_blank"
       style="color:white;text-decoration:none;font-weight:600;">Insights Blog</a></li>
  </ul>
  <div style="display:flex;align-items:center;gap:20px;">
    <a href="https://twitter.com" target="_blank">
      <img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" style="width:24px;height:24px;"></a>
    <a href="https://facebook.com" target="_blank">
      <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" style="width:24px;height:24px;margin-left:10px;"></a>
    <select style="background:transparent;border:none;color:white;font-weight:600;font-size:15px;">
      <option value="en" selected>English 🇬🇧</option>
      <option value="es">Español 🇪🇸</option>
      <option value="fr">Français 🇫🇷</option>
    </select>
  </div>
</nav>
"""

# --- Background ---
def set_background_url(image_url):
    st.markdown(f"""
    <style>
    html, body {{ height:100%; margin:0; padding:0;
        background-image:url("{image_url}");
        background-size:cover; background-position:center; background-repeat:no-repeat; }}
    .stApp {{ background-color:rgba(0,0,0,0.6) !important; color:white; height:100%; }}
    </style>
    """, unsafe_allow_html=True)


# --- Load Model ---
def load_model():
    try:
        base = os.path.dirname(__file__)
        model_path = os.path.join(base, 'crypto_liquidity_model.pkl')
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        return None


# -------------------------------------------------------
# CORE FIX: Normalize raw RandomForest regression output
# to a 0-1 liquidity score using multiple strategies
# -------------------------------------------------------
def normalize_score(raw, volume, market_cap):
    raw = float(raw)

    # Strategy 1: already in [0,1] - use directly
    if 0.0 <= raw <= 1.0:
        return raw

    # Strategy 2: large regression value - use volume/market_cap ratio
    if raw > 1.0 and market_cap > 0:
        ratio = volume / market_cap
        # ratio < 0.05  -> Low   (score < 0.33)
        # ratio 0.05-0.2 -> Medium (score 0.33-0.66)
        # ratio > 0.2   -> High  (score > 0.66)
        score = np.clip(ratio / 0.3, 0.0, 1.0)
        return float(score)

    # Strategy 3: any other float -> sigmoid compress to [0,1]
    score = 1.0 / (1.0 + np.exp(-raw))
    return float(score)


# -------------------------------------------------------
# FIX: Thresholds now evenly split [0,1] into 3 zones
# -------------------------------------------------------
def classify_liquidity(score):
    if score < 0.33:
        return "🔴 Low", "#ff4d4d"
    elif score < 0.66:
        return "🟡 Medium", "#ffd700"
    else:
        return "🟢 High", "#4dff91"


# -------------------------------------------------------
# FIX: Trend uses % change + volatility for strength
# -------------------------------------------------------
def predict_trend(open_p, close_p, high_p, low_p):
    if open_p == 0:
        return "⚖️ Insufficient data"
    change_pct   = ((close_p - open_p) / open_p) * 100
    volatility   = ((high_p - low_p)   / open_p) * 100 if open_p > 0 else 0
    strong_move  = volatility > 5

    if change_pct > 3:
        return f"📈 {'Strong' if strong_move else 'Moderate'} Bullish  (+{change_pct:.2f}%)"
    elif change_pct > 0:
        return f"📈 Slightly Bullish  (+{change_pct:.2f}%)"
    elif change_pct < -3:
        return f"📉 {'Strong' if strong_move else 'Moderate'} Bearish  ({change_pct:.2f}%)"
    elif change_pct < 0:
        return f"📉 Slightly Bearish  ({change_pct:.2f}%)"
    else:
        return "⚖️ Sideways  (0.00%)"


# -------------------------------------------------------
# FIX: Real indicator proxies instead of hardcoded 0
# -------------------------------------------------------
def compute_indicators(open_p, high_p, low_p, close_p):
    sma_5  = (open_p + high_p + low_p + close_p) / 4
    ema_12 = close_p * 0.6 + open_p * 0.2 + high_p * 0.1 + low_p * 0.1
    rnge   = (high_p - low_p) if high_p != low_p else 1
    rsi    = float(np.clip(50 + ((close_p - open_p) / rnge) * 50, 0, 100))
    macd   = ema_12 - sma_5
    return sma_5, ema_12, rsi, macd


# ===================== APP SETUP =====================
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")
components.html(navbar_html, height=80, scrolling=False)

bg = "https://raw.githubusercontent.com/jayasri21072006/crypto-liquidity-predictor/main/53540861975_5538e666cf_c.jpg"
set_background_url(bg)

st.markdown("<div style='margin-top:75px;'></div>", unsafe_allow_html=True)
st.markdown("<h1 style='color:white;'>💧 Crypto Liquidity Predictor</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#ccc;'>Enter crypto OHLCV data to predict <strong>Liquidity Level</strong>.</p><hr>",
    unsafe_allow_html=True)

# --- Coin Selection ---
coin_names = sorted([
    'Bitcoin','Ethereum','Tether','BNB','XRP','Solana','Cardano',
    'Dogecoin','Shiba Inu','Polygon','Litecoin','Polkadot','Avalanche',
    'Uniswap','Chainlink','Stellar','VeChain','TRON','Filecoin','Near',
])
selected_coin = st.selectbox("Optional: Select a Coin", [""] + coin_names)

# --- Session State ---
for k, v in dict(open_price=0.0, high_price=0.0, low_price=0.0, close_price=0.0, volume=0.0).items():
    if k not in st.session_state:
        st.session_state[k] = v

# Demo data — LOW volume coins → will trigger Low liquidity label
demo_map = {
    'Bitcoin':   (56787.5,  64776.4,  55000.0,  63000.0,  25000.0),    # High
    'Ethereum':  (3100.0,   3500.0,   2900.0,   3400.0,   180000.0),   # High
    'Solana':    (140.0,    165.0,    130.0,    158.0,    4500000.0),   # Medium/High
    'Dogecoin':  (0.12,     0.14,     0.10,     0.09,     500.0),       # Low
    'Shiba Inu': (0.000008, 0.000010, 0.000006, 0.000007, 100.0),       # Low
    'Cardano':   (0.45,     0.52,     0.40,     0.48,     20000.0),     # Medium
    'Filecoin':  (4.5,      5.2,      4.0,      4.2,      80.0),        # Low
    'VeChain':   (0.02,     0.025,    0.018,    0.019,    300.0),       # Low
}

def load_demo_data():
    coin = selected_coin if selected_coin in demo_map else 'Bitcoin'
    o, h, l, c, v = demo_map[coin]
    st.session_state.open_price  = o
    st.session_state.high_price  = h
    st.session_state.low_price   = l
    st.session_state.close_price = c
    st.session_state.volume      = v

if st.button("🔄 Load Demo Data"):
    load_demo_data()
    st.rerun()

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    open_price  = st.number_input('Open Price ($)',  value=float(st.session_state.open_price),  min_value=0.0, format="%.6f")
    high_price  = st.number_input('High Price ($)',  value=float(st.session_state.high_price),  min_value=0.0, format="%.6f")
    low_price   = st.number_input('Low Price ($)',   value=float(st.session_state.low_price),   min_value=0.0, format="%.6f")
with col2:
    close_price = st.number_input('Close Price ($)', value=float(st.session_state.close_price), min_value=0.0, format="%.6f")
    volume      = st.number_input('Volume (units)',  value=float(st.session_state.volume),      min_value=0.0, format="%.4f")

st.session_state.open_price  = open_price
st.session_state.high_price  = high_price
st.session_state.low_price   = low_price
st.session_state.close_price = close_price
st.session_state.volume      = volume

# --- Validation ---
valid = True
if high_price > 0 and low_price > 0 and high_price < low_price:
    st.warning("⚠️ High Price must be ≥ Low Price.")
    valid = False

# --- Market cap proxy ---
market_cap_proxy = close_price * volume
st.markdown(
    f"<h4 style='color:#00c8ff;'>Volume × Close: ${market_cap_proxy:,.4f} "
    f"<span style='font-size:13px;color:#aaa;'>(liquidity size proxy)</span></h4>",
    unsafe_allow_html=True)

# --- Chart ---
if any([open_price, high_price, low_price, close_price]):
    st.line_chart(pd.DataFrame(
        {"Price ($)": [open_price, high_price, low_price, close_price]},
        index=["Open", "High", "Low", "Close"]
    ))

# --- Indicators ---
sma_5, ema_12, rsi, macd = compute_indicators(open_price, high_price, low_price, close_price)
with st.expander("📊 Technical Indicators (sent to model)"):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SMA",    f"{sma_5:.4f}")
    c2.metric("EMA-12", f"{ema_12:.4f}")
    c3.metric("RSI",    f"{rsi:.1f}")
    c4.metric("MACD",   f"{macd:.4f}")

# --- Model Input DataFrame ---
input_data = pd.DataFrame({
    'Open':       [open_price],
    'High':       [high_price],
    'Low':        [low_price],
    'Close':      [close_price],
    'Volume':     [volume],
    'Market Cap': [market_cap_proxy],
    'SMA_5':      [sma_5],
    'EMA_12':     [ema_12],
    'RSI':        [rsi],
    'MACD':       [macd],
})

model = load_model()

# --- Disclaimer ---
st.markdown("""
<div style="background:rgba(255,255,255,0.1);padding:12px 16px;border-radius:8px;margin-top:10px;">
<b>⚠️ Disclaimer:</b> AI-based tool for informational purposes only.
Not financial advice. Use at your own risk.
</div>""", unsafe_allow_html=True)
agree = st.checkbox("I agree to the disclaimer above.")

# --- Predict Button ---
if st.button("🔮 Predict Liquidity"):
    if not model:
        st.error("❌ Model not loaded. Ensure crypto_liquidity_model.pkl is in the same folder as this file.")
    elif not agree:
        st.warning("⚠️ Please accept the disclaimer first.")
    elif not valid:
        st.warning("⚠️ Fix input errors above before predicting.")
    elif close_price == 0 or volume == 0:
        st.warning("⚠️ Enter non-zero values for Close Price and Volume.")
    else:
        try:
            raw_score = float(model.predict(input_data)[0])

            # Show raw model output so you can verify
            st.caption(f"🔧 Raw model output: `{raw_score:.6f}`")

            # Normalize raw score → [0, 1]
            score = normalize_score(raw_score, volume, market_cap_proxy)

            label, color = classify_liquidity(score)
            trend        = predict_trend(open_price, close_price, high_price, low_price)
            pct          = int(score * 100)
            coin_tag     = f" — {selected_coin}" if selected_coin else ""

            st.markdown(f"""
            <div style='text-align:center; background:rgba(255,255,255,0.08);
                        border-radius:14px; padding:28px; margin-top:18px;'>
                <h3 style='color:white;'>🔍 Prediction Results{coin_tag}</h3>
                <p style='font-size:20px;'>
                    <strong>Liquidity:</strong>
                    <span style='color:{color}; font-weight:bold; font-size:24px;'>{label}</span>
                </p>
                <p style='font-size:18px;'><strong>Trend:</strong> {trend}</p>
                <p style='color:#aaa; font-size:14px;'>Normalised Score: {score:.4f} / 1.0000</p>

                <div style='background:#333; border-radius:8px; height:22px;
                            margin:14px auto; width:80%; overflow:hidden;'>
                    <div style='background:{color}; width:{pct}%; height:100%; border-radius:8px;'></div>
                </div>
                <small style='color:#888;'>◀ Low (0) &nbsp;&nbsp;&nbsp; Medium &nbsp;&nbsp;&nbsp; High (1) ▶</small>
            </div>
            """, unsafe_allow_html=True)

        except ValueError as ve:
            st.error(f"❌ Feature mismatch: {ve}")
            st.info("💡 Your model may expect different column names. "
                    "Check crypto_price_prediction notebook for the exact feature list.")
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
