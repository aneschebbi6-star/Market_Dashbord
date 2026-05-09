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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; font-family: 'Inter', sans-serif; }
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

def _inject_login_styles():
    """Inject premium login page CSS with animated background and glassmorphism."""
    st.markdown("""
    <style>
    /* ── Hide Streamlit defaults on login ── */
    [data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* ── Animated background ── */
    .login-bg {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0;
        background: radial-gradient(ellipse at 20% 50%, #1a1a4e 0%, transparent 50%),
                    radial-gradient(ellipse at 80% 20%, #0c2340 0%, transparent 50%),
                    radial-gradient(ellipse at 50% 80%, #1e0a3c 0%, transparent 50%),
                    linear-gradient(160deg, #070b1a 0%, #0d1b2a 40%, #0a0e1a 100%);
        overflow: hidden;
    }
    .login-bg .orb {
        position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.4;
        animation: float-orb 12s ease-in-out infinite alternate;
    }
    .login-bg .orb:nth-child(1) { width: 400px; height: 400px; top: -100px; left: -80px; background: radial-gradient(circle, #3b82f6, transparent 70%); animation-duration: 14s; }
    .login-bg .orb:nth-child(2) { width: 350px; height: 350px; bottom: -60px; right: -60px; background: radial-gradient(circle, #8b5cf6, transparent 70%); animation-delay: -4s; animation-duration: 16s; }
    .login-bg .orb:nth-child(3) { width: 250px; height: 250px; top: 40%; left: 60%; background: radial-gradient(circle, #06b6d4, transparent 70%); animation-delay: -8s; animation-duration: 18s; }
    @keyframes float-orb {
        0%   { transform: translate(0, 0) scale(1); }
        33%  { transform: translate(30px, -40px) scale(1.05); }
        66%  { transform: translate(-20px, 20px) scale(0.95); }
        100% { transform: translate(15px, -15px) scale(1.02); }
    }
    .login-bg::after {
        content: ''; position: absolute; inset: 0;
        background-image: linear-gradient(rgba(59, 130, 246, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(59, 130, 246, 0.03) 1px, transparent 1px);
        background-size: 60px 60px;
    }

    /* ── Card: style the Streamlit column itself ── */
    [data-testid="column"].login-col-target {
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 24px !important;
        padding: 2.5rem 2rem !important;
        box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.12),
                    0 20px 60px -15px rgba(0, 0, 0, 0.65),
                    0 0 50px rgba(59, 130, 246, 0.06) !important;
        animation: card-appear 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
        opacity: 0 !important; transform: translateY(28px) !important;
        margin-top: 8vh !important;
    }
    @keyframes card-appear { to { opacity: 1 !important; transform: translateY(0) !important; } }

    .login-title {
        font-family: 'Inter', sans-serif !important; font-weight: 800 !important; font-size: 1.65rem !important;
        background: linear-gradient(135deg, #60a5fa, #a78bfa, #c084fc) !important;
        -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
        text-align: center; margin: 0 0 0.25rem 0; letter-spacing: -0.02em;
    }
    .login-subtitle {
        text-align: center; color: rgba(148, 163, 184, 0.65); font-size: 0.78rem;
        margin-bottom: 0; font-weight: 400; letter-spacing: 0.07em; text-transform: uppercase;
    }
    .login-divider {
        height: 1px; background: linear-gradient(90deg, transparent, rgba(59,130,246,0.35), transparent);
        margin: 1.4rem 0 1.6rem 0;
    }
    /* hide empty stElementContainers from markdown-only calls */
    [data-testid="column"].login-col-target [data-testid="stElementContainer"]:empty,
    [data-testid="column"].login-col-target [data-testid="stElementContainer"]:has(p:empty) {
        display: none !important;
    }

    /* ── Inputs ── */
    .login-card-premium [data-testid="stTextInput"] > div > div {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 12px !important; padding: 4px 10px !important;
        transition: all 0.25s ease !important;
    }
    .login-card-premium [data-testid="stTextInput"] > div > div:focus-within {
        border-color: rgba(59, 130, 246, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12) !important;
        background: rgba(30, 41, 59, 0.85) !important;
    }
    .login-card-premium [data-testid="stTextInput"] input { color: #e2e8f0 !important; font-family: 'Inter', sans-serif !important; font-size: 0.95rem !important; }
    .login-card-premium [data-testid="stTextInput"] label { color: rgba(148, 163, 184, 0.85) !important; font-weight: 600 !important; font-size: 0.75rem !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }

    /* ── Button ── */
    .login-card-premium .stButton > button {
        width: 100%; padding: 0.9rem 1.5rem !important;
        border-radius: 12px !important; font-size: 0.9rem !important;
        font-weight: 700 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important;
        background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
        border: none !important; color: white !important;
        box-shadow: 0 4px 24px rgba(59, 130, 246, 0.35) !important;
        transition: all 0.25s ease !important; margin-top: 0.5rem !important;
    }
    .login-card-premium .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.5) !important;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    }

    /* ── Status ── */
    .login-status {
        display: flex; justify-content: center; gap: 1.5rem;
        margin-top: 1.8rem; padding-top: 1.2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    .login-status .status-item { display: flex; align-items: center; gap: 5px; font-size: 0.68rem; color: rgba(148, 163, 184, 0.55); text-transform: uppercase; letter-spacing: 0.06em; }
    .dot { width: 5px; height: 5px; border-radius: 50%; animation: blink-dot 2s ease-in-out infinite; }
    .dot-green { background: #22c55e; }
    .dot-blue  { background: #3b82f6; }
    @keyframes blink-dot { 0%, 100% { opacity: 1; } 50% { opacity: 0.25; } }

    /* ── Error ── */
    .login-card-premium [data-testid="stAlert"] {
        background: rgba(239, 68, 68, 0.08) !important;
        border: 1px solid rgba(239, 68, 68, 0.25) !important;
        border-radius: 10px !important; margin-top: 0.5rem !important;
    }

    /* ── Ticker tape ── */
    .ticker-tape {
        position: fixed; top: 0; left: 0; width: 100%; height: 36px;
        background: rgba(10, 14, 26, 0.9); backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(59, 130, 246, 0.15);
        overflow: hidden; z-index: 100; display: flex; align-items: center;
    }
    .ticker-content {
        display: flex; gap: 3rem; white-space: nowrap;
        animation: scroll-ticker 25s linear infinite;
        font-size: 0.72rem; font-family: 'Inter', monospace; font-weight: 500;
    }
    .ticker-item { color: rgba(148, 163, 184, 0.7); }
    .ticker-item .sym { color: #60a5fa; margin-right: 4px; }
    .ticker-item .up  { color: #22c55e; }
    .ticker-item .dn  { color: #f87171; }
    @keyframes scroll-ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
    </style>
    """, unsafe_allow_html=True)

# ── CONTROLLER : AUTHENTIFICATION ─────────────────────

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    _inject_login_styles()

    now = time.strftime('%H:%M:%S')
    ticker_html = "".join([
        '<span class="ticker-item"><span class="sym">BTC</span><span class="up">▲ +2.34%</span></span>',
        '<span class="ticker-item"><span class="sym">ETH</span><span class="up">▲ +1.87%</span></span>',
        '<span class="ticker-item"><span class="sym">SOL</span><span class="dn">▼ -0.52%</span></span>',
        '<span class="ticker-item"><span class="sym">BNB</span><span class="up">▲ +0.91%</span></span>',
        '<span class="ticker-item"><span class="sym">XRP</span><span class="dn">▼ -1.14%</span></span>',
        '<span class="ticker-item"><span class="sym">ADA</span><span class="up">▲ +3.07%</span></span>',
        '<span class="ticker-item"><span class="sym">DOGE</span><span class="up">▲ +0.44%</span></span>',
    ])

    st.markdown(f"""
    <div class="login-bg"><div class="orb"></div><div class="orb"></div><div class="orb"></div></div>
    <div class="ticker-tape"><div class="ticker-content">{ticker_html}{ticker_html}</div></div>
    <div style="height: 52px;"></div>
    """, unsafe_allow_html=True)

    _, login_col, _ = st.columns([1, 1.1, 1])

    # Inject JS to add a CSS class to the middle column so we can target it
    st.markdown("""
    <script>
    (function() {
        function tagLoginCol() {
            var cols = document.querySelectorAll('[data-testid="column"]');
            if (cols.length >= 2) { cols[1].classList.add('login-col-target'); }
        }
        if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', tagLoginCol); }
        else { tagLoginCol(); }
        setTimeout(tagLoginCol, 300);
    })();
    </script>
    """, unsafe_allow_html=True)

    with login_col:
        st.markdown("""
        <div class="login-title">Market Dashboard Pro</div>
        <div class="login-subtitle">Terminal de Trading Sécurisé</div>
        <div class="login-divider"></div>
        """, unsafe_allow_html=True)

        user = st.text_input("👤  Identifiant", placeholder="Nom d'utilisateur", key="login_user")
        pwd  = st.text_input("🔑  Mot de Passe", type="password", placeholder="Mot de passe", key="login_pwd")

        if st.button("🔓  ACCÉDER AU TERMINAL", use_container_width=True, key="login_btn"):
            if user == "Anes0123" and pwd == "chebbi@1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("⛔ Accès refusé — Identifiants invalides")

        st.markdown(f"""
        <div class="login-status">
            <div class="status-item"><span class="dot dot-green"></span> En ligne</div>
            <div class="status-item"><span class="dot dot-blue"></span> Chiffré</div>
            <div class="status-item">{now}</div>
        </div>
        """, unsafe_allow_html=True)

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
