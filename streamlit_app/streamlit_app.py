import streamlit as st

st.markdown("""
<style>
.background-watermark {
    position: fixed;
    top: 50%;
    left: 50%;
    width: 300px;
    height: 300px;
    background-image: url('https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=024');
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    opacity: 0.07;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: -1;
}
body {
    background-color: #f9fafb;
    padding: 20px;
}
</style>
<div class="background-watermark"></div>
""", unsafe_allow_html=True)

st.title("Check if Bitcoin watermark appears")
st.write("If you do not see the watermark, try refreshing or check your network.")
