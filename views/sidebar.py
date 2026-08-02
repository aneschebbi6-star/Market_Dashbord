import streamlit as st
import re
import time

# Popular tickers the user can pick from.  Ordered by market-cap / popularity
# so the most common choices appear first.  The special sentinel "✏️ Autre…"
# lets users type a custom ticker that isn't in the list.
POPULAR_TICKERS = [
    "BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "AVAX", "DOT", "MATIC",
    "LINK", "SHIB", "LTC", "UNI", "ATOM", "FIL", "APT", "ARB", "OP", "NEAR",
    "GOLD", "SILVER", "OIL",
]

_CUSTOM_SENTINEL = "✏️ Autre…"

# Only uppercase letters, digits, dash, dot, equals (covers "BTC", "GC=F", etc.)
_TICKER_RE = re.compile(r"^[A-Z0-9.\-=]{1,12}$")


def _validate_ticker(raw: str) -> str | None:
    """Return a cleaned ticker string or *None* if the input is invalid."""
    cleaned = raw.strip().upper()
    if not cleaned:
        return None
    if _TICKER_RE.match(cleaned):
        return cleaned
    return None


def render_sidebar():
    """Render the sidebar for user inputs."""
    with st.sidebar:
        st.title("⚙️ Pilotage")
        st.divider()

        page = st.radio(
            "Page",
            options=["Dashboard", "Portefeuille"],
            index=0,
            horizontal=True,
            key="app_page",
        )
        st.divider()

        if page == "Portefeuille":
            st.markdown("**Gérez votre portefeuille et suivez vos positions en temps réel.**")
            st.caption("Ajoutez des transactions ou affichez la performance globale de votre portefeuille.")
            st.divider()

            if st.button("🔄 Actualiser Flux", use_container_width=True):
                st.rerun()
            if st.button("🚪 Quitter la Session", use_container_width=True):
                st.session_state["password_correct"] = False
                st.rerun()

            st.caption(f"Status : Connecté | {time.strftime('%H:%M:%S')}")
            return page, "", "", True, False, "Candlestick"

        # ── Ticker principal ────────────────────────────────────────────
        st.subheader("🔍 Analyse Ticker")

        choice = st.selectbox(
            "Ticker",
            options=POPULAR_TICKERS + [_CUSTOM_SENTINEL],
            index=0,  # default = BTC
            help="Choisissez un actif populaire ou sélectionnez « Autre » pour saisir un ticker personnalisé.",
        )

        if choice == _CUSTOM_SENTINEL:
            custom_raw = st.text_input(
                "Ticker personnalisé",
                value="",
                placeholder="ex: NEAR, FTM, AAPL",
                max_chars=12,
            )
            ticker = _validate_ticker(custom_raw)
            if custom_raw and ticker is None:
                st.warning("⚠️ Ticker invalide — utilisez uniquement des lettres, chiffres, « - », « . » ou « = ».")
                ticker = "BTC"  # safe fallback
        else:
            ticker = choice.upper()

        # ── Ticker de comparaison ───────────────────────────────────────
        compare_choice = st.selectbox(
            "Comparer avec (Optionnel)",
            options=["Aucun"] + POPULAR_TICKERS + [_CUSTOM_SENTINEL],
            index=0,
            help="Sélectionnez un second actif pour comparer les performances.",
        )

        if compare_choice == _CUSTOM_SENTINEL:
            compare_raw = st.text_input(
                "Ticker de comparaison personnalisé",
                value="",
                placeholder="ex: ETH, SOL",
                max_chars=12,
            )
            compare_ticker = _validate_ticker(compare_raw) or ""
            if compare_raw and not compare_ticker:
                st.warning("⚠️ Ticker de comparaison invalide.")
        elif compare_choice == "Aucun":
            compare_ticker = ""
        else:
            compare_ticker = compare_choice.upper()

        # ── Outils graphiques ───────────────────────────────────────────
        st.divider()
        st.subheader("Outils Graphiques")
        ma50 = st.checkbox("Moyenne Mobile 50", value=True)
        ma200 = st.checkbox("Moyenne Mobile 200", value=False)
        chart_type = st.radio(
            "Type de graphique",
            options=["Candlestick", "Line", "Area"],
            index=0,
            horizontal=True,
        )

        # ── Actions ────────────────────────────────────────────────────
        st.divider()
        if st.button("🔄 Actualiser Flux", use_container_width=True):
            st.rerun()
        if st.button("🚪 Quitter la Session", use_container_width=True):
            st.session_state["password_correct"] = False
            st.rerun()
        st.caption(f"Status : Connecté | {time.strftime('%H:%M:%S')}")
        return page, ticker, compare_ticker, ma50, ma200, chart_type
