import streamlit as st
from styles.theme import inject_global_styles
from controllers.auth import check_password
from views.sidebar import render_sidebar
from views.dashboard import render_metrics, render_chart, render_footer_table
from fetcher import get_prices

def setup_page():
    st.set_page_config(page_title="Market Dashboard Pro", layout="wide", initial_sidebar_state="collapsed")
    inject_global_styles()

def main():
    try:
        setup_page()
        
        if not check_password():
            st.stop()

        # Controller: Data Fetching
        top_symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "ADA-USD", "DOGE-USD"]
        data = get_prices(top_symbols)
        
        if not data:
            st.error("Erreur de flux de données.")
            return

        # View: Rendering
        search_ticker, show_ma50, show_ma200 = render_sidebar()
        
        st.title("🚀 Market Dashboard Pro")
        render_metrics(data)
        st.divider()
        render_chart(search_ticker, show_ma50, show_ma200)
        render_footer_table(data)
    except Exception as e:
        st.error(f"Une erreur interne est survenue : {e}")
        st.exception(e)

if __name__ == "__main__":
    main()