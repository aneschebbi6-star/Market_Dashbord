import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from cache_layer import cached_get_history, cached_get_news
from fetcher import analyze_sentiment

def render_metrics(data):
    """Render the top metric cards."""
    metric_items = [
        ("BITCOIN (BTC)", "btc"),
        ("ETHEREUM (ETH)", "eth"),
        ("SOLANA (SOL)", "sol"),
        ("OR (GOLD)", "gold"),
        ("ARGENT (SILVER)", "silver"),
        ("PÉTROLE (OIL)", "oil")
    ]

    def fmt(key):
        if key in data:
            return f"${data[key]['usd']:,.2f}", f"{data[key]['usd_24h_change']:.2f}%"
        return "$0.00", "0.00%"

    for row_start in range(0, len(metric_items), 3):
        cols = st.columns(3)
        for col, (label, key) in zip(cols, metric_items[row_start:row_start + 3]):
            price, change = fmt(key)
            col.metric(label, price, change)

def build_chart(
    hist,
    show_ma50=False,
    show_ma200=False,
    show_rsi=False,
    show_macd=False,
    show_bb=False,
    chart_type="Candlestick",
):
    if hist.empty:
        return go.Figure().update_layout(
            template="plotly_dark",
            title="Aucune donnée disponible",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=30, r=20, t=40, b=20),
        )

    rows = 2
    row_heights = [0.55, 0.15]
    subplot_titles = ["Prix", "Volume"]

    has_rsi = show_rsi and "RSI" in hist.columns
    has_macd = show_macd and "MACD" in hist.columns

    if has_rsi:
        rows += 1
        row_heights.append(0.15)
        subplot_titles.append("RSI")
    if has_macd:
        rows += 1
        row_heights.append(0.15)
        subplot_titles.append("MACD")

    fig = make_subplots(
        rows=rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=row_heights,
        subplot_titles=subplot_titles,
    )

    if chart_type == "Candlestick":
        fig.add_trace(
            go.Candlestick(
                x=hist.index,
                open=hist["Open"],
                high=hist["High"],
                low=hist["Low"],
                close=hist["Close"],
                name="Prix",
                increasing_line_color="#22c55e",
                decreasing_line_color="#ef4444",
            ),
            row=1,
            col=1,
        )
    elif chart_type == "Line":
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["Close"],
                mode="lines",
                name="Clôture",
                line=dict(color="#2196f3", width=2),
            ),
            row=1,
            col=1,
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["Close"],
                mode="lines",
                name="Clôture",
                line=dict(color="#2196f3", width=2),
                fill="tozeroy",
                fillcolor="rgba(33, 150, 243, 0.15)",
            ),
            row=1,
            col=1,
        )

    if show_bb and "BB_High" in hist.columns:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["BB_High"],
                mode="lines",
                name="BB Haut",
                line=dict(color="#ff9800", dash="dot", width=1),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["BB_Mid"],
                mode="lines",
                name="BB Moy",
                line=dict(color="#ffb74d", dash="dash", width=1),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["BB_Low"],
                mode="lines",
                name="BB Bas",
                line=dict(color="#ff9800", dash="dot", width=1),
                fill="tonexty",
                fillcolor="rgba(255, 152, 0, 0.08)",
            ),
            row=1,
            col=1,
        )

    if show_ma50 and "MA50" in hist.columns:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["MA50"],
                name="MA 50",
                line=dict(color="#fbbf24", width=2),
            ),
            row=1,
            col=1,
        )
    if show_ma200 and "MA200" in hist.columns:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["MA200"],
                name="MA 200",
                line=dict(color="#f87171", width=2),
            ),
            row=1,
            col=1,
        )

    volume_colors = [
        "#22c55e" if c >= o else "#ef4444"
        for c, o in zip(hist["Close"], hist["Open"])
    ]
    fig.add_trace(
        go.Bar(
            x=hist.index,
            y=hist["Volume"],
            name="Volume",
            marker_color=volume_colors,
            opacity=0.65,
        ),
        row=2,
        col=1,
    )

    current_row = 3
    if has_rsi:
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["RSI"],
                mode="lines",
                name="RSI",
                line=dict(color="#9c27b0", width=2),
            ),
            row=current_row,
            col=1,
        )
        fig.add_hline(y=70, line_dash="dot", line_color="#ef5350", row=current_row, col=1)
        fig.add_hline(y=30, line_dash="dot", line_color="#22c55e", row=current_row, col=1)
        fig.update_yaxes(range=[0, 100], row=current_row, col=1)
        current_row += 1

    if has_macd:
        if "MACD_Hist" not in hist.columns and "MACD" in hist.columns and "MACD_Signal" in hist.columns:
            hist["MACD_Hist"] = hist["MACD"] - hist["MACD_Signal"]

        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["MACD"],
                mode="lines",
                name="MACD",
                line=dict(color="#00bcd4", width=2),
            ),
            row=current_row,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["MACD_Signal"],
                mode="lines",
                name="Signal MACD",
                line=dict(color="#ff5722", width=1.5, dash="dash"),
            ),
            row=current_row,
            col=1,
        )
        fig.add_trace(
            go.Bar(
                x=hist.index,
                y=hist["MACD_Hist"],
                name="Histogramme MACD",
                marker_color=["#22c55e" if v >= 0 else "#ef4444" for v in hist["MACD_Hist"]],
                opacity=0.6,
            ),
            row=current_row,
            col=1,
        )

    fig.update_layout(
        template="plotly_dark",
        height=200 + 120 * rows,
        margin=dict(l=40, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)")
    return fig


def build_comparison_chart(main_ticker, compare_ticker, period_label):
    hist_main = cached_get_history(main_ticker, period_label)
    hist_compare = cached_get_history(compare_ticker, period_label)

    if hist_main.empty or hist_compare.empty:
        return None

    main_data, compare_data = (
        hist_main[["Close", "Volume"]].align(
            hist_compare[["Close", "Volume"]], join="inner"
        )
    )

    if main_data.empty or compare_data.empty:
        return None

    perf_main = (main_data["Close"] / main_data["Close"].iloc[0] - 1) * 100
    perf_compare = (compare_data["Close"] / compare_data["Close"].iloc[0] - 1) * 100

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.65, 0.25],
        subplot_titles=["Performance (%)", "Volume"],
    )

    fig.add_trace(
        go.Scatter(
            x=perf_main.index,
            y=perf_main,
            name=main_ticker,
            line=dict(color="#fbbf24", width=2),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=perf_compare.index,
            y=perf_compare,
            name=compare_ticker,
            line=dict(color="#3b82f6", width=2),
        ),
        row=1,
        col=1,
    )
    fig.add_hline(y=0, line_dash="dot", line_color="gray", row=1, col=1)

    fig.add_trace(
        go.Bar(
            x=main_data.index,
            y=main_data["Volume"],
            name=f"Volume {main_ticker}",
            marker_color="rgba(251, 189, 36, 0.5)",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=compare_data.index,
            y=compare_data["Volume"],
            name=f"Volume {compare_ticker}",
            marker_color="rgba(59, 130, 246, 0.5)",
        ),
        row=2,
        col=1,
    )

    fig.update_layout(
        template="plotly_dark",
        height=520,
        margin=dict(l=40, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)")
    return fig


def render_chart(ticker, compare_ticker, show_ma50, show_ma200, chart_type):
    """Render the main trading chart."""
    st.subheader(f"📊 Analyse Technique : {ticker}")
    p_map = {"1J": "1J", "7J": "7J", "1M": "1M", "1A": "1A"}

    col1, col2 = st.columns([1, 2])
    with col1:
        sel_p = st.radio("Sélecteur de Temps", options=list(p_map.keys()), index=1, horizontal=True)
    with col2:
        selected_indicators = st.multiselect(
            "Indicateurs Techniques",
            options=["RSI", "MACD", "Bandes de Bollinger"],
            default=[],
        )

    df_hist = cached_get_history(ticker, period_label=sel_p)

    if sel_p == "1J":
        st.info("⚠️ Mode intraday (5 min) — les bougies peuvent être incomplètes en dehors des heures de marché.")

    if not df_hist.empty:
        fig = build_chart(
            df_hist,
            show_ma50=show_ma50,
            show_ma200=show_ma200,
            show_rsi="RSI" in selected_indicators,
            show_macd="MACD" in selected_indicators,
            show_bb="Bandes de Bollinger" in selected_indicators,
            chart_type=chart_type,
        )
        # Display which interval was actually used (may differ for commodities)
        interval_used = df_hist.attrs.get('interval_used') if hasattr(df_hist, 'attrs') else None
        if interval_used:
            st.caption(f"Interval utilisé: {interval_used}")

        # Inform user if MA50/MA200 are unavailable for this timeframe and show EMA fallback
        ma_notes = []
        if show_ma50 and ('MA50' not in df_hist.columns or df_hist['MA50'].isna().all()):
            ma_notes.append("MA50 non disponible pour cette période (insufficient bars). Affichage de EMA20 à la place.")
        if show_ma200 and ('MA200' not in df_hist.columns or df_hist['MA200'].isna().all()):
            ma_notes.append("MA200 non disponible pour cette période (insufficient bars). Affichage de EMA20 à la place.")
        if ma_notes:
            for note in ma_notes:
                st.info(note)

        st.plotly_chart(fig, use_container_width=True)

        if compare_ticker:
            fig_comp = build_comparison_chart(ticker, compare_ticker, sel_p)
            if fig_comp is not None:
                st.divider()
                st.subheader(f"🔄 Comparaison : {ticker} vs {compare_ticker} (Performance %)")
                st.plotly_chart(fig_comp, use_container_width=True)
            else:
                st.warning(f"Unable to compare {ticker} with {compare_ticker} : pas assez de données communes.")
    else:
        st.warning(f"Ticker '{ticker}' introuvable.")

def _format_change_label(change):
    arrow = "▲" if change >= 0 else "▼"
    return f"{arrow} {change:.2f}%"


def _render_market_overview(data):
    sorted_items = sorted(data.items(), key=lambda item: item[1].get('usd_24h_change', 0))
    if not sorted_items:
        return

    top_loser = sorted_items[0]
    top_gainer = sorted_items[-1]
    avg_change = sum(item[1].get('usd_24h_change', 0) for item in sorted_items) / len(sorted_items)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="📉 Meilleure baisse",
            value=top_loser[0].upper(),
            delta=_format_change_label(top_loser[1].get('usd_24h_change', 0)),
        )
    with col2:
        st.metric(
            label="📈 Meilleure hausse",
            value=top_gainer[0].upper(),
            delta=_format_change_label(top_gainer[1].get('usd_24h_change', 0)),
        )
    with col3:
        st.metric(
            label="⚖️ Variation moyenne 24h",
            value=_format_change_label(avg_change),
            delta="",
        )


def render_footer_table(data):
    """Render the data table expander with enhanced market details."""
    with st.expander("🔍 Voir le Détail du Marché"):
        st.write(
            "**Aperçu du marché en un coup d'œil** : trouvez rapidement les actifs les plus dynamiques et suivez la performance globale.")
        st.divider()
        _render_market_overview(data)

        st.markdown("### Tableau des actifs")
        table_data = []
        for k, v in data.items():
            change = v.get('usd_24h_change', 0.0)
            # signed formatted percentage
            change_str = f"{change:+.2f}%"
            table_data.append(
                {
                    "ACTIF": k.upper(),
                    "VALEUR ($)": f"{v['usd']:,.2f}",
                    "CHANGE 24H": change_str,
                    "CHANGE_FLOAT": change,
                    "STATUT": "Hausse" if change >= 0 else "Baisse",
                }
            )

        df = pd.DataFrame(table_data)

        # Sort by numeric change to avoid lexicographic ordering of percentage strings
        if 'CHANGE_FLOAT' in df.columns:
            df = df.sort_values(by='CHANGE_FLOAT', ascending=False)

        # Prefer AgGrid for interactive table if available, otherwise fallback to st.dataframe
        try:
            from st_aggrid import AgGrid, GridOptionsBuilder

            gb = GridOptionsBuilder.from_dataframe(df.drop(columns=['CHANGE_FLOAT']))
            gb.configure_default_column(filter=True, sortable=True)
            gb.configure_column('CHANGE 24H', header_name='CHANGE 24H')
            grid_options = gb.build()
            AgGrid(
                df.drop(columns=['CHANGE_FLOAT']),
                gridOptions=grid_options,
                enable_enterprise_modules=False,
                fit_columns_on_grid_load=True,
                height=300,
            )
        except Exception:
            # st_aggrid not installed — simple fallback
            df = df.drop(columns=['CHANGE_FLOAT'])
            st.dataframe(df, use_container_width=True)

        st.markdown(
            "_Astuce : cliquez sur les en-têtes de colonnes pour trier les actifs par prix ou variation._"
        )


def render_sentiment_gauge(ticker):
    """Render sentiment analysis gauge for a cryptocurrency.
    
    Args:
        ticker: Crypto ticker symbol (e.g., 'BTC', 'ETH')
    """
    st.subheader("🎯 Analyse de Sentiment (Actualités)")
    
    with st.spinner(f"Chargement des actualités pour {ticker}..."):
        # Fetch news
        crypto_mapping = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "SOL": "solana",
            "BNB": "binancecoin",
            "XRP": "ripple",
            "ADA": "cardano",
            "DOGE": "dogecoin",
            "GOLD": "gold",
            "GC=F": "gold",
            "SILVER": "silver",
            "SI=F": "silver",
            "OIL": "oil",
            "CL=F": "oil"
        }
        
        crypto_name = crypto_mapping.get(ticker.upper(), ticker.lower())

        news = cached_get_news(crypto_name, limit=10)
        
        if not news or len(news) == 0:
            st.info(f"⏳ Aucune actualité disponible pour {ticker} en ce moment.")
            return
        
        sentiment_result = analyze_sentiment(news)
        
        # Display gauge
        gauge_col, info_col = st.columns([2, 1])
        
        with gauge_col:
            # Create gauge figure
            sentiment_score = sentiment_result['score']
            sentiment_label = sentiment_result['label']
            
            # Color based on sentiment
            if sentiment_label == 'Bullish':
                gauge_color = '#22c55e'
            elif sentiment_label == 'Bearish':
                gauge_color = '#ef4444'
            else:
                gauge_color = '#94a3b8'
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=sentiment_score * 100,  # Scale to -100 to 100
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"Sentiment Score"},
                delta={'reference': 0, 'suffix': " pts"},
                gauge={
                    'axis': {'range': [-100, 100]},
                    'bar': {'color': gauge_color},
                    'steps': [
                        {'range': [-100, -33], 'color': 'rgba(239, 68, 68, 0.2)'},
                        {'range': [-33, 33], 'color': 'rgba(148, 163, 184, 0.2)'},
                        {'range': [33, 100], 'color': 'rgba(34, 197, 94, 0.2)'}
                    ],
                    'threshold': {
                        'line': {'color': 'white', 'width': 2},
                        'thickness': 0.75,
                        'value': 0
                    }
                }
            ))
            
            fig_gauge.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=30, b=0)
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with info_col:
            st.metric("Sentiment Global", sentiment_label, f"{sentiment_score:.3f}")
        
        # Display top 3 impactful news
        st.divider()
        st.subheader("📰 Actualités Principales")
        
        # Sort by absolute sentiment score to get most impactful
        sorted_articles = sorted(
            sentiment_result['articles'],
            key=lambda x: abs(x['sentiment_score']),
            reverse=True
        )[:3]
        
        for idx, article in enumerate(sorted_articles, 1):
            with st.container():
                col1, col2 = st.columns([3, 1], gap="large")
                
                with col1:
                    sentiment_emoji = "📈" if article['sentiment_label'] == 'Bullish' else "📉" if article['sentiment_label'] == 'Bearish' else "➡️"
                    
                    st.markdown(
                        f"**{idx}. {sentiment_emoji} {article['title'][:80]}...**"
                        if len(article['title']) > 80
                        else f"**{idx}. {sentiment_emoji} {article['title']}**"
                    )
                    
                    st.caption(f"Source: {article['source']} • Score: {article['sentiment_score']:.2f}")
                    
                    if article.get('url'):
                        st.markdown(f"[Lire l'article →]({article['url']})", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"<div style='text-align: center; padding: 10px; background: rgba({128 if article['color'] == 'green' else 239 if article['color'] == 'red' else 148}, {197 if article['color'] == 'green' else 68 if article['color'] == 'red' else 163}, {94 if article['color'] == 'green' else 68 if article['color'] == 'red' else 184}, 0.1); border-radius: 8px;'><strong>{article['sentiment_label']}</strong></div>", unsafe_allow_html=True)
                
            st.divider()
