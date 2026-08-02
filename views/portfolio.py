import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from controllers.portfolio import add_position, load_portfolio, portfolio_snapshot, remove_position


def _validate_number(value, field_name: str) -> float | None:
    try:
        converted = float(value)
        if converted <= 0:
            st.warning(f"{field_name} doit être supérieur à 0.")
            return None
        return converted
    except Exception:
        st.warning(f"{field_name} doit être un nombre valide.")
        return None


def _format_currency(value: float) -> str:
    return f"${value:,.2f}"


def render_portfolio_page():
    st.title("💼 Simulateur de Portefeuille")
    st.markdown(
        "Gérez vos positions, suivez votre coût moyen, et comparez la valeur actuelle avec vos prix d'achat."
    )
    st.divider()

    with st.form("portfolio_entry_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            ticker = st.text_input("Ticker", value="BTC", max_chars=12)
        with col2:
            quantity = st.text_input("Quantité", value="1.0")
        with col3:
            purchase_price = st.text_input("Prix d'achat ($)", value="1000.0")

        submitted = st.form_submit_button("Ajouter la position")

    if submitted:
        ticker_str = ticker.strip().upper()
        quantity_val = _validate_number(quantity, "Quantité")
        purchase_price_val = _validate_number(purchase_price, "Prix d'achat")

        if quantity_val is not None and purchase_price_val is not None:
            add_position(ticker_str, quantity_val, purchase_price_val, date.today())
            st.success(f"Position ajoutée : {ticker_str} x {quantity_val} @ ${purchase_price_val:.2f}")
            st.experimental_rerun()

    positions = load_portfolio()
    if not positions:
        st.info("Aucune position enregistrée. Ajoutez une transaction pour commencer votre simulation.")
        return

    df = portfolio_snapshot()
    total_cost = df.attrs.get("total_cost", 0.0)
    total_value = df.attrs.get("total_value", 0.0)
    total_pnl = total_value - total_cost
    total_pnl_pct = (total_pnl / total_cost * 100) if total_cost else 0.0

    st.subheader("Résumé du Portefeuille")
    col1, col2, col3 = st.columns(3)
    col1.metric("Coût total", _format_currency(total_cost), "")
    col2.metric("Valeur actuelle", _format_currency(total_value), "")
    col3.metric("PnL total", _format_currency(total_pnl), f"{total_pnl_pct:.2f}%")

    if not df.empty:
        with st.expander("Répartition du portefeuille"):
            pie_df = df[df["Valeur actuelle ($)"] > 0][["Ticker", "Valeur actuelle ($)"]].copy()
            if not pie_df.empty:
                fig = px.pie(
                    pie_df,
                    names="Ticker",
                    values="Valeur actuelle ($)",
                    title="Répartition de la valeur actuelle",
                    hole=0.45,
                )
                fig.update_traces(textposition="inside", textinfo="percent+label")
                fig.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune valeur actuelle positive à afficher pour la répartition.")

    st.divider()
    st.subheader("Détails des Positions")

    visible_df = df.drop(columns=[col for col in df.columns if col == "Date d'achat"]) if "Date d'achat" in df.columns else df
    st.dataframe(visible_df, use_container_width=True)

    if not df.empty:
        with st.expander("Voir toutes les positions et supprimer une position"):
            for idx, row in df.reset_index(drop=True).iterrows():
                cols = st.columns([3, 1, 1, 1])
                with cols[0]:
                    st.markdown(
                        "**{}** — {} unités @ {}".format(
                            row['Ticker'],
                            row['Quantité'],
                            _format_currency(row['Prix d\'achat ($)'])
                        )
                    )
                    st.caption("Acheté le {}".format(row["Date d'achat"]))
                with cols[1]:
                    st.write(f"Valeur actuelle: {_format_currency(row['Valeur actuelle ($)'])}")
                with cols[2]:
                    st.write(f"PnL: {_format_currency(row['PnL ($)'])} / {row['PnL (%)']:.2f}%")
                with cols[3]:
                    if st.button(f"Supprimer #{idx+1}", key=f"remove_{idx}"):
                        remove_position(idx)
                        st.success(f"Position #{idx+1} supprimée.")
                        st.experimental_rerun()

    st.divider()
    st.markdown(
        "_Conseil : utilisez un ticker compatible Yahoo Finance, par exemple BTC, ETH, SOL, ou des symboles de matières premières comme GOLD, SILVER, OIL._"
    )
