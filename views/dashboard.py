import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

def render_chart(ticker, compare_ticker, show_ma50, show_ma200):
    """Render the main trading chart."""
    st.subheader(f"📊 Analyse Technique : {ticker}")
    p_map = {"1J": 1, "7J": 7, "1M": 30, "1A": 365}
    
    col1, col2 = st.columns([1, 2])
    with col1:
        sel_p = st.radio("Sélecteur de Temps", options=list(p_map.keys()), index=1, horizontal=True)
    with col2:
        selected_indicators = st.multiselect(
            "Indicateurs Techniques",
            options=["RSI", "MACD", "Bandes de Bollinger"],
            default=[]
        )
        
    df_hist = get_history(ticker, days=p_map[sel_p])

    if not df_hist.empty:
        df_hist['MA50'] = df_hist['Close'].rolling(window=50).mean()
        df_hist['MA200'] = df_hist['Close'].rolling(window=200).mean()
        
        # Création de la figure avec un axe Y secondaire pour les oscillateurs (RSI/MACD)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Candlestick principal
        fig.add_trace(go.Candlestick(x=df_hist.index, open=df_hist['Open'], high=df_hist['High'], low=df_hist['Low'], close=df_hist['Close'], name='Prix'), secondary_y=False)
        
        # Moyennes mobiles
        if show_ma50: fig.add_trace(go.Scatter(x=df_hist.index, y=df_hist['MA50'], line=dict(color='#fbbf24', width=2), name='MA 50'), secondary_y=False)
        if show_ma200: fig.add_trace(go.Scatter(x=df_hist.index, y=df_hist['MA200'], line=dict(color='#f87171', width=2), name='MA 200'), secondary_y=False)
        
        # Bandes de Bollinger
        if "Bandes de Bollinger" in selected_indicators and 'BB_High' in df_hist.columns:
            fig.add_trace(go.Scatter(x=df_hist.index, y=df_hist['BB_High'], line=dict(color='rgba(255, 255, 255, 0.3)', width=1, dash='dash'), name='BB High'), secondary_y=False)
            fig.add_trace(go.Scatter(x=df_hist.index, y=df_hist['BB_Low'], line=dict(color='rgba(255, 255, 255, 0.3)', width=1, dash='dash'), name='BB Low', fill='tonexty', fillcolor='rgba(255, 255, 255, 0.05)'), secondary_y=False)
            fig.add_trace(go.Scatter(x=df_hist.index, y=df_hist['BB_Mid'], line=dict(color='rgba(255, 255, 255, 0.5)', width=1), name='BB Mid'), secondary_y=False)

        # Oscillateurs (RSI et MACD) sur l'axe Y secondaire
        if "RSI" in selected_indicators and 'RSI' in df_hist.columns:
            fig.add_trace(go.Scatter(x=df_hist.index, y=df_hist['RSI'], line=dict(color='#a855f7', width=2), name='RSI'), secondary_y=True)

        if "MACD" in selected_indicators and 'MACD' in df_hist.columns:
            fig.add_trace(go.Scatter(x=df_hist.index, y=df_hist['MACD'], line=dict(color='#3b82f6', width=2), name='MACD'), secondary_y=True)
            fig.add_trace(go.Scatter(x=df_hist.index, y=df_hist['MACD_Signal'], line=dict(color='#ef4444', width=2), name='Signal MACD'), secondary_y=True)
            fig.add_trace(go.Bar(x=df_hist.index, y=df_hist['MACD_Diff'], name='Histogramme MACD', marker_color='#22c55e', opacity=0.5), secondary_y=True)

        # Mise en forme globale
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=600, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        
        # Cacher la grille de l'axe Y secondaire pour plus de clarté
        fig.update_yaxes(showgrid=False, secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Section Comparaison
        if compare_ticker:
            df_compare = get_history(compare_ticker, days=p_map[sel_p])
            if not df_compare.empty:
                st.divider()
                st.subheader(f"🔄 Comparaison : {ticker} vs {compare_ticker} (Performance %)")
                
                # Normalisation Base 100
                base_price_main = df_hist['Close'].iloc[0]
                base_price_comp = df_compare['Close'].iloc[0]
                
                df_hist['Normalized'] = (df_hist['Close'] / base_price_main) * 100
                df_compare['Normalized'] = (df_compare['Close'] / base_price_comp) * 100
                
                fig_comp = go.Figure()
                fig_comp.add_trace(go.Scatter(x=df_hist.index, y=df_hist['Normalized'], name=ticker, line=dict(color='#fbbf24', width=2)))
                fig_comp.add_trace(go.Scatter(x=df_compare.index, y=df_compare['Normalized'], name=compare_ticker, line=dict(color='#3b82f6', width=2)))
                
                # Mise en forme globale
                fig_comp.update_layout(
                    template="plotly_dark", 
                    height=450, 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)', 
                    margin=dict(l=0, r=0, t=30, b=0), 
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    yaxis_title="Performance (Base 100)"
                )
                
                st.plotly_chart(fig_comp, use_container_width=True)
            else:
                st.warning(f"Ticker de comparaison '{compare_ticker}' introuvable ou pas assez de données.")

    else:
        st.warning(f"Ticker '{ticker}' introuvable.")

def render_footer_table(data):
    """Render the data table expander."""
    with st.expander("🔍 Voir le Détail du Marché"):
        table_data = [{"ACTIF": k.upper(), "VALEUR ($)": f"{v['usd']:,.2f}", "CHANGE 24H": f"{v['usd_24h_change']:.2f}%"} for k, v in data.items()]
        st.table(pd.DataFrame(table_data))
