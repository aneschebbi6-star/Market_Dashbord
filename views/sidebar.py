import streamlit as st
import time

def render_sidebar():
    """Render the sidebar for user inputs."""
    with st.sidebar:
        st.title("⚙️ Pilotage")
        st.divider()
        st.subheader("🔍 Analyse Ticker")
        ticker = st.text_input("Ticker", value="BTC", placeholder="ex: DOGE, ADA").upper()
        compare_ticker = st.text_input("Comparer avec (Optionnel)", value="", placeholder="ex: ETH, SOL").upper()
        st.divider()
        st.subheader("Outils Graphiques")
        ma50 = st.checkbox("Moyenne Mobile 50", value=True)
        ma200 = st.checkbox("Moyenne Mobile 200", value=False)
        st.divider()
        if st.button("🔄 Actualiser Flux", use_container_width=True):
            st.rerun()
        if st.button("🚪 Quitter la Session", use_container_width=True):
            st.session_state["password_correct"] = False
            st.rerun()
        st.caption(f"Status : Connecté | {time.strftime('%H:%M:%S')}")
        return ticker, compare_ticker, ma50, ma200
