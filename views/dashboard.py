import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fetcher import get_history

def render_metrics(data):
    """Render the top metric cards."""
    m_col1, m_col2, m_col3 = st.columns(3)
    def fmt(key):
        if key in data:
            return f"${data[key]['usd']:,.2f}", f"{data[key]['usd_24h_change']:.2f}%"
        return "$0.00", "0.00%"
    
    p1, c1 = fmt("btc")
    p2, c2 = fmt("eth")
    p3, c3 = fmt("sol")
    
    m_col1.metric("BITCOIN (BTC)", p1, c1)
    m_col2.metric("ETHEREUM (ETH)", p2, c2)
    m_col3.metric("SOLANA (SOL)", p3, c3)

def render_chart(ticker, show_ma50, show_ma200):
    """Render the main trading chart."""
    st.subheader(f"📊 Analyse Technique : {ticker}")
    p_map = {"1J": 1, "7J": 7, "1M": 30, "1A": 365}
    sel_p = st.radio("Sélecteur de Temps", options=list(p_map.keys()), index=1, horizontal=True)
    df_hist = get_history(ticker, days=p_map[sel_p])

    if not df_hist.empty:
        df_hist['MA50'] = df_hist['Close'].rolling(window=50).mean()
        df_hist['MA200'] = df_hist['Close'].rolling(window=200).mean()
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df_hist.index, open=df_hist['Open'], high=df_hist['High'], low=df_hist['Low'], close=df_hist['Close'], name='Prix'))
        if show_ma50: fig.add_trace(go.Scatter(x=df_hist.index, y=df_hist['MA50'], line=dict(color='#fbbf24', width=2), name='MA 50'))
        if show_ma200: fig.add_trace(go.Scatter(x=df_hist.index, y=df_hist['MA200'], line=dict(color='#f87171', width=2), name='MA 200'))
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=550, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Ticker '{ticker}' introuvable.")

def render_footer_table(data):
    """Render the data table expander."""
    with st.expander("🔍 Voir le Détail du Marché"):
        table_data = [{"ACTIF": k.upper(), "VALEUR ($)": f"{v['usd']:,.2f}", "CHANGE 24H": f"{v['usd_24h_change']:.2f}%"} for k, v in data.items()]
        st.table(pd.DataFrame(table_data))
