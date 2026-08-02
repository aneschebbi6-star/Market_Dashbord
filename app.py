import streamlit as st
from styles.theme import inject_global_styles
from views.sidebar import render_sidebar
from views.dashboard import render_metrics, render_chart, render_footer_table, render_sentiment_gauge
from views.portfolio import render_portfolio_page
from cache_layer import cached_get_prices

def setup_page():
    st.set_page_config(page_title="Market Dashboard Pro", layout="wide", initial_sidebar_state="collapsed")
    inject_global_styles()

def main():
    try:
        setup_page()

        # View: Sidebar and navigation
        sidebar_result = render_sidebar()
        if isinstance(sidebar_result, tuple) and len(sidebar_result) == 6:
            page, search_ticker, compare_ticker, show_ma50, show_ma200, chart_type = sidebar_result
        else:
            page = "Dashboard"
            search_ticker, compare_ticker, show_ma50, show_ma200, chart_type = "BTC", "", True, False, "Candlestick"

        if page == "Portefeuille":
            render_portfolio_page()
            return

        # Controller: Data Fetching
        top_symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "GC=F", "SI=F", "CL=F"]
        data = cached_get_prices(top_symbols)
        
        if not data:
            st.error("Erreur de flux de données.")
            return

        # View: Rendering
        st.title("🚀 Market Dashboard Pro")
        render_metrics(data)
        st.divider()
        render_chart(search_ticker, compare_ticker, show_ma50, show_ma200, chart_type)
        st.divider()
        render_sentiment_gauge(search_ticker)
        st.divider()
        render_footer_table(data)
    except Exception as e:
        st.error(f"Une erreur interne est survenue : {e}")
        st.exception(e)

if __name__ == "__main__":
    main()