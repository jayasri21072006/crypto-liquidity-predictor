import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import numpy as np
import os

# --- Navbar HTML ---
navbar_html = """
<nav style="background-color:#102a44; color:white; display:flex; align-items:center; padding:12px 30px; justify-content:space-between; border-radius:0 0 10px 10px; box-shadow:0 4px 8px rgba(0,0,0,0.1); font-family: 'Poppins', Arial, sans-serif; width: 100vw; position: fixed; top: 0; left: 0; z-index: 9999; box-sizing: border-box;">
  <div style="display:flex; align-items:center;">
    <div style="font-weight:700; font-size:26px; background: linear-gradient(90deg, #34e89e, #0f3443); -webkit-background-clip: text; -webkit-text-fill-color: transparent; user-select:none; cursor:default;">CryptoPredictions</div>
  </div>
  <ul class="nav-links" style="list-style:none; display:flex; gap: 25px; margin:0; padding:0;">
    <li><a href="https://cryptonews.com" target="_blank" style="color:white; text-decoration:none; font-weight:600;">Market Updates</a></li>
    <li><a href="https://cryptopredictions.com/?results=200" target="_blank" style="color:white; text-decoration:none; font-weight:600;">Coin List</a></li>
    <li><a href="https://cryptopredictions.com/blog/" target="_blank" style="color:white; text-decoration:none; font-weight:600;">Insights Blog</a></li>
  </ul>
  <div style="display:flex; align-items:center; gap:20px;">
    <div>
      <a href="https://twitter.com" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" style="width:24px; height:24px;"></a>
      <a href="https://facebook.com" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" style="width:24px; height:24px; margin-left: 10px;"></a>
    </div>
    <select style="background:transparent; border:none; color:white; font-weight:600; font-size:15px;">
      <option value="en" selected>English 🇬🇧</option>
      <option value="es">Español 🇪🇸</option>
      <option value="fr">Français 🇫🇷</option>
    </select>
  </div>
</nav>
"""

# --- Set Background ---
def set_background_url(image_url):
    css = f"""
    <style>
    html, body {{
        height: 100%;
        margin: 0;
        padding: 0;
        background-image: url("{image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .stApp {{
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white;
        height: 100%;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# --- Load Model ---
def load_model():
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'crypto_liquidity_model.pkl')
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        return None


# -------------------------------------------------------
# FIX 1: classify_liquidity now normalises the raw score
# before applying thresholds so Low CAN be returned.
# -------------------------------------------------------
def normalize_score(raw_score, volume, market_cap):
    """
    Normalize raw model output to a 0-1 liquidity score.
    Strategy: use volume-to-market-cap ratio as the primary signal.
    If the model outputs a ratio-like value we scale it directly;
    otherwise we derive a ratio ourselves.
    """
    # If raw_score is already in [0, 1] trust it
    if 0.0 <= raw_score <= 1.0:
        return float(raw_score)

    # If raw_score looks like a large dollar value (e.g. regression on price),
    # fall back to a volume/market_cap liquidity ratio
    if market_cap > 0:
        ratio = volume / market_cap          # typically 0.01 – 0.5 for crypto
        # clip and scale: ratio >= 0.5 => high, < 0.1 => low
        score = np.clip(ratio / 0.5, 0.0, 1.0)
        return float(score)

    # Last resort: min-max compress around the raw score
    score = 1 / (1 + np.exp(-raw_score / 1e4))  # sigmoid squeeze
    return float(score)


def classify_liquidity(score):
    """
    Classify a normalised [0,1] score into Low / Medium / High.
    Thresholds chosen so that all three classes are reachable.
    """
    if score < 0.35:
        return "<span style='color:#ff4d4d; font-weight:bold;'>🔴 Low</span>"
    elif score < 0.65:
        return "<span style='color:#ffd700; font-weight:bold;'>🟡 Medium</span>"
    else:
        return "<span style='color:#4dff91; font-weight:bold;'>🟢 High</span>"


# -------------------------------------------------------
# FIX 2: predict_trend uses price change % + volume signal
# -------------------------------------------------------
def predict_trend(open_p, close_p, volume, avg_volume_estimate=None):
    """
    More realistic trend: combines price direction with volume confirmation.
    """
    if open_p == 0:
        return "⚖️ Insufficient data for trend analysis"

    change_pct = ((close_p - open_p) / open_p) * 100

    # Volume confirmation: if volume is unusually high, trend is stronger
    if avg_volume_estimate and avg_volume_estimate > 0:
        vol_ratio = volume / avg_volume_estimate
        vol_note = " (high volume confirms move)" if vol_ratio > 1.5 else \
                   " (low volume — weak signal)" if vol_ratio < 0.5 else ""
    else:
        vol_note = ""

    if change_pct > 1.0:
        return f"📈 Bullish — up {change_pct:.2f}%{vol_note}"
    elif change_pct < -1.0:
        return f"📉 Bearish — down {abs(change_pct):.2f}%{vol_note}"
    else:
        return f"⚖️ Sideways — change {change_pct:.2f}%{vol_note}"


# -------------------------------------------------------
# FIX 3: Compute real technical indicators instead of 0s
# -------------------------------------------------------
def compute_indicators(open_p, high_p, low_p, close_p, volume):
    """
    Approximate single-candle technical indicators.
    These are rough proxies — in production, use a rolling price history.
    """
    prices = [open_p, high_p, low_p, close_p]

    # Simple Moving Average (proxy: avg of OHLC)
    sma_5 = np.mean(prices)

    # EMA_12 proxy: weighted toward close
    ema_12 = (close_p * 0.6 + open_p * 0.2 + high_p * 0.1 + low_p * 0.1)

    # RSI proxy: based on body vs wick ratio
    body = abs(close_p - open_p)
    total_range = high_p - low_p if high_p != low_p else 1
    rsi = 50 + (((close_p - open_p) / total_range) * 50)  # maps to [0, 100]
    rsi = float(np.clip(rsi, 0, 100))

    # MACD proxy: EMA12 - SMA5
    macd = ema_12 - sma_5

    return sma_5, ema_12, rsi, macd


# --- App Setup ---
st.set_page_config(page_title="Crypto Liquidity Predictor", page_icon="💧", layout="centered")
components.html(navbar_html, height=80, scrolling=False)

background_img_url = "https://raw.githubusercontent.com/jayasri21072006/crypto-liquidity-predictor/main/53540861975_5538e666cf_c.jpg"
set_background_url(background_img_url)

# --- Title ---
st.markdown("<div style='margin-top:70px;'></div>", unsafe_allow_html=True)
st.markdown("<h1 style='color:white;'>💧 Crypto Liquidity Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#ccc;'>Enter crypto OHLCV data to estimate <strong>Liquidity Level</strong> and price trend.</p><hr>", unsafe_allow_html=True)

# --- Coin Selection ---
coin_names = sorted([
    'Bitcoin', 'Ethereum', 'Tether', 'BNB', 'XRP', 'Solana', 'Cardano',
    'Dogecoin', 'Shiba Inu', 'Polygon', 'Litecoin', 'Polkadot', 'Avalanche',
    'Uniswap', 'Chainlink', 'Stellar', 'VeChain', 'TRON', 'Filecoin', 'Near',
])
selected_coin = st.selectbox("Optional: Select a Coin", [""] + coin_names)

# --- Session State Defaults ---
for key, default in [
    ('open_price', 0.0), ('high_price', 0.0), ('low_price', 0.0),
    ('close_price', 0.0), ('volume', 0.0)
]:
    if key not in st.session_state:
        st.session_state[key] = default

# --- Demo Data Presets per Coin ---
demo_data_map = {
    'Bitcoin':   (56787.5, 64776.4, 55000.0, 63000.0, 123456.789),
    'Ethereum':  (3100.0,  3500.0,  2900.0,  3400.0,  890234.0),
    'Solana':    (140.0,   165.0,   130.0,   158.0,   4500000.0),
    'Dogecoin':  (0.12,    0.18,    0.10,    0.09,    9800000000.0),   # Low liquidity example
    'Shiba Inu': (0.000008, 0.000012, 0.000006, 0.000007, 500000000000.0),
}

def load_demo_data():
    coin = selected_coin if selected_coin in demo_data_map else 'Bitcoin'
    o, h, l, c, v = demo_data_map[coin]
    st.session_state.open_price  = o
    st.session_state.high_price  = h
    st.session_state.low_price   = l
    st.session_state.close_price = c
    st.session_state.volume      = v

if st.button("🔄 Load Demo Data"):
    load_demo_data()
    st.rerun()

# --- Input Fields ---
col1, col2 = st.columns(2)
with col1:
    open_price  = st.number_input('Open Price ($)',  value=float(st.session_state.open_price),  min_value=0.0, format="%.6f")
    high_price  = st.number_input('High Price ($)',  value=float(st.session_state.high_price),  min_value=0.0, format="%.6f")
    low_price   = st.number_input('Low Price ($)',   value=float(st.session_state.low_price),   min_value=0.0, format="%.6f")
with col2:
    close_price = st.number_input('Close Price ($)', value=float(st.session_state.close_price), min_value=0.0, format="%.6f")
    volume      = st.number_input('Volume',          value=float(st.session_state.volume),      min_value=0.0, format="%.4f")

# Update session state
st.session_state.open_price  = open_price
st.session_state.high_price  = high_price
st.session_state.low_price   = low_price
st.session_state.close_price = close_price
st.session_state.volume      = volume

# -------------------------------------------------------
# FIX 4: Input validation — high must be >= low, etc.
# -------------------------------------------------------
input_valid = True
if high_price < low_price and (high_price > 0 or low_price > 0):
    st.warning("⚠️ High Price should be greater than or equal to Low Price.")
    input_valid = False
if open_price > 0 and not (low_price <= open_price <= high_price):
    st.warning("⚠️ Open Price should be between Low and High.")
    input_valid = False
if close_price > 0 and not (low_price <= close_price <= high_price):
    st.warning("⚠️ Close Price should be between Low and High.")
    input_valid = False

# --- Market Cap ---
# FIX 5: Label correctly as "Volume × Close" proxy, not true market cap
volume_x_close = close_price * volume
st.markdown(
    f"<h4 style='color:#00c8ff;'>Volume × Close Price: ${volume_x_close:,.2f} "
    f"<span style='font-size:13px; color:#aaa;'>(proxy for liquidity size)</span></h4>",
    unsafe_allow_html=True
)

# --- Price Chart ---
if any([open_price, high_price, low_price, close_price]):
    price_df = pd.DataFrame(
        {"Price ($)": [open_price, high_price, low_price, close_price]},
        index=["Open", "High", "Low", "Close"]
    )
    st.line_chart(price_df)

# --- Compute Indicators ---
sma_5, ema_12, rsi, macd = compute_indicators(open_price, high_price, low_price, close_price, volume)

# Show computed indicators to user
with st.expander("📊 Computed Technical Indicators (used by model)"):
    ic1, ic2, ic3, ic4 = st.columns(4)
    ic1.metric("SMA (proxy)", f"{sma_5:,.4f}")
    ic2.metric("EMA-12 (proxy)", f"{ema_12:,.4f}")
    ic3.metric("RSI (proxy)", f"{rsi:.1f}")
    ic4.metric("MACD (proxy)", f"{macd:,.4f}")

# --- Model Input ---
input_data = pd.DataFrame({
    'Open':       [open_price],
    'High':       [high_price],
    'Low':        [low_price],
    'Close':      [close_price],
    'Volume':     [volume],
    'Market Cap': [volume_x_close],
    'SMA_5':      [sma_5],
    'EMA_12':     [ema_12],
    'RSI':        [rsi],
    'MACD':       [macd]
})

# --- Load Model ---
model = load_model()

# --- Disclaimer ---
st.markdown("""
<div style="background-color: rgba(255,255,255,0.1); padding: 12px 16px; border-radius: 8px; margin-top:10px;">
<b>⚠️ Disclaimer:</b> This is an AI-based tool. Predictions are for informational purposes only
and do not constitute financial advice. Use at your own risk.
</div>
""", unsafe_allow_html=True)
agree = st.checkbox("I agree to the disclaimer above.")

# --- Predict ---
if st.button("🔮 Predict Liquidity"):
    if not model:
        st.error("❌ Model not loaded. Ensure crypto_liquidity_model.pkl is in the same directory.")
    elif not agree:
        st.warning("⚠️ You must accept the disclaimer to proceed.")
    elif not input_valid:
        st.warning("⚠️ Please fix the input errors above before predicting.")
    elif close_price == 0 or volume == 0:
        st.warning("⚠️ Please enter non-zero values for Close Price and Volume.")
    else:
        try:
            raw_score = model.predict(input_data)[0]

            # DEBUG: show raw model output (remove in production if desired)
            st.caption(f"🔧 Raw model output: `{raw_score}`")

            # Normalize to [0, 1]
            score = normalize_score(raw_score, volume, volume_x_close)

            liquidity_html = classify_liquidity(score)
            trend          = predict_trend(open_price, close_price, volume)

            # Liquidity gauge bar
            pct = int(score * 100)
            bar_color = "#ff4d4d" if score < 0.35 else "#ffd700" if score < 0.65 else "#4dff91"

            st.markdown(f"""
            <div style='text-align:center; background:rgba(255,255,255,0.08);
                        border-radius:12px; padding:24px; margin-top:16px;'>
                <h3 style='color:white;'>🔍 Prediction Results
                    {f"— <span style='font-size:18px;'>{selected_coin}</span>" if selected_coin else ""}
                </h3>
                <p style='font-size:18px;'><strong>Liquidity Level:</strong> {liquidity_html}</p>
                <p style='font-size:18px;'><strong>Trend:</strong> {trend}</p>
                <p style='font-size:15px; color:#aaa;'>Normalised Liquidity Score: {score:.3f} / 1.000</p>

                <div style='background:#222; border-radius:8px; height:18px; margin:10px auto; width:80%; overflow:hidden;'>
                    <div style='background:{bar_color}; width:{pct}%; height:100%;
                                border-radius:8px; transition:width 0.5s ease;'></div>
                </div>
                <small style='color:#888;'>0 ← Low &nbsp;&nbsp;&nbsp; Medium &nbsp;&nbsp;&nbsp; High → 100</small>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
            st.info("💡 Make sure your model was trained with the same 10 features: "
                    "Open, High, Low, Close, Volume, Market Cap, SMA_5, EMA_12, RSI, MACD")
