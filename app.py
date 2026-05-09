import streamlit as st
from datetime import datetime
import pandas as pd
from fetcher import get_prices, get_history
import time
import plotly.graph_objects as go

# ── CONFIGURATION & STYLE ────────────────────────────

def setup_page():
    st.set_page_config(page_title="Market Dashboard Pro", layout="wide", initial_sidebar_state="collapsed")
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
        .login-card {
            background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px);
            padding: 3rem; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); width: 100%; max-width: 450px;
        }
        [data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.5); backdrop-filter: blur(5px);
            padding: 20px !important; border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important; transition: transform 0.3s ease;
        }
        [data-testid="stMetric"]:hover { transform: translateY(-5px); border-color: #3b82f6 !important; }
        [data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.95) !important; border-right: 1px solid rgba(255, 255, 255, 0.1) !important; }
        h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; background: linear-gradient(to right, #60a5fa, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .stButton>button { border-radius: 10px !important; background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%) !important; color: white !important; border: none !important; font-weight: 600 !important; padding: 0.5rem 2rem !important; }
        </style>
        """, unsafe_allow_html=True)

# ── CONTROLLER : AUTHENTIFICATION ─────────────────────

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.write("## 🔒 Terminal Sécurisé")
        st.caption("Entrez vos identifiants pour accéder au Dashboard")
        user = st.text_input("Username", placeholder="Nom d'utilisateur")
        pwd = st.text_input("Password", type="password", placeholder="Mot de passe")
        if st.button("AUTHENTIFICATION", use_container_width=True):
            if user == "Anes0123" and pwd == "chebbi@1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Accès refusé : Identifiants invalides")
        st.markdown('</div>', unsafe_allow_html=True)
    return False

# ── VIEW : COMPOSANTS UI ──────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Pilotage")
        st.divider()
        st.subheader("🔍 Analyse Ticker")
        ticker = st.text_input("Ticker", value="BTC", placeholder="ex: DOGE, ADA").upper()
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
        return ticker, ma50, ma200

def render_metrics(data):
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
    with st.expander("🔍 Voir le Détail du Marché"):
        table_data = [{"ACTIF": k.upper(), "VALEUR ($)": f"{v['usd']:,.2f}", "CHANGE 24H": f"{v['usd_24h_change']:.2f}%"} for k, v in data.items()]
        st.table(pd.DataFrame(table_data))

# ── MAIN APPLICATION ─────────────────────────────────

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
