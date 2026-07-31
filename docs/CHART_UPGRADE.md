# Patch Guide — `dashboard.py` Chart / Candlestick Improvements

> Apply each section independently. Every block shows **what to replace** and **what to put instead**.

---

## A. Corriger le chargement de données (`get_history`)

### Avant
```python
def get_history(ticker, period="1mo"):
    hist = ticker.history(period=period)
    ...
```

### Après
```python
PERIOD_CONFIG = {
    "1J":  {"period": "1d",  "interval": "5m"},
    "7J":  {"period": "7d",  "interval": "1h"},
    "1M":  {"period": "1mo", "interval": "1d"},
    "3M":  {"period": "3mo", "interval": "1d"},
    "1A":  {"period": "1y",  "interval": "1d"},
    "5A":  {"period": "5y",  "interval": "1wk"},
}

def get_history(ticker, period_label="1M"):
    cfg = PERIOD_CONFIG.get(period_label, {"period": "1mo", "interval": "1d"})
    hist = ticker.history(period=cfg["period"], interval=cfg["interval"])

    if hist.empty:
        return hist  # géré en aval

    # Calcul des indicateurs — uniquement si assez de données
    if len(hist) >= 14:
        delta = hist["Close"].diff()
        gain  = delta.clip(lower=0).rolling(14).mean()
        loss  = (-delta.clip(upper=0)).rolling(14).mean()
        rs    = gain / loss
        hist["RSI"] = 100 - (100 / (1 + rs))

        ema12 = hist["Close"].ewm(span=12, adjust=False).mean()
        ema26 = hist["Close"].ewm(span=26, adjust=False).mean()
        hist["MACD"]        = ema12 - ema26
        hist["MACD_signal"] = hist["MACD"].ewm(span=9, adjust=False).mean()

    if len(hist) >= 20:
        sma20 = hist["Close"].rolling(20).mean()
        std20 = hist["Close"].rolling(20).std()
        hist["BB_upper"] = sma20 + 2 * std20
        hist["BB_lower"] = sma20 - 2 * std20
        hist["BB_mid"]   = sma20

    return hist
```

---

## B. Améliorer le graphique principal (`build_chart`)

### Avant
```python
def build_chart(hist, show_rsi=False, show_macd=False, show_bb=False):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=hist.index,
        open=hist["Open"], high=hist["High"],
        low=hist["Low"],   close=hist["Close"],
        name="Prix"
    ))
    # RSI / MACD ajoutés sur le même axe...
```

### Après
```python
from plotly.subplots import make_subplots

def build_chart(hist, show_rsi=False, show_macd=False, show_bb=False, chart_type="Candlestick"):
    if hist.empty:
        return go.Figure().update_layout(title="Aucune donnée disponible")

    # ── Nombre de sous-graphiques ──────────────────────────────────────────
    rows        = 2  # candlestick + volume toujours présents
    row_heights = [0.55, 0.15]
    subplot_titles = ["Prix", "Volume"]

    has_rsi  = show_rsi  and "RSI"  in hist.columns
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
        rows=rows, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=row_heights,
        subplot_titles=subplot_titles,
    )

    # ── Graphique principal ────────────────────────────────────────────────
    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=hist.index,
            open=hist["Open"], high=hist["High"],
            low=hist["Low"],   close=hist["Close"],
            name="Prix",
            increasing_line_color="#26a69a",   # vert
            decreasing_line_color="#ef5350",   # rouge
            increasing_fillcolor="#26a69a",
            decreasing_fillcolor="#ef5350",
        ), row=1, col=1)
    elif chart_type == "Line":
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist["Close"],
            mode="lines", name="Clôture",
            line=dict(color="#2196F3", width=1.5),
        ), row=1, col=1)
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist["Close"],
            mode="lines", fill="tozeroy", name="Clôture",
            line=dict(color="#2196F3", width=1.5),
            fillcolor="rgba(33, 150, 243, 0.15)",
        ), row=1, col=1)

    # ── Bollinger Bands ────────────────────────────────────────────────────
    if show_bb and "BB_upper" in hist.columns:
        for col, label, dash in [
            ("BB_upper", "BB Haut", "dot"),
            ("BB_mid",   "BB Moy",  "dash"),
            ("BB_lower", "BB Bas",  "dot"),
        ]:
            fig.add_trace(go.Scatter(
                x=hist.index, y=hist[col],
                mode="lines", name=label,
                line=dict(color="#FF9800", dash=dash, width=1),
            ), row=1, col=1)

    # ── Volume ─────────────────────────────────────────────────────────────
    colors = [
        "#26a69a" if c >= o else "#ef5350"
        for c, o in zip(hist["Close"], hist["Open"])
    ]
    fig.add_trace(go.Bar(
        x=hist.index, y=hist["Volume"],
        name="Volume", marker_color=colors, opacity=0.7,
    ), row=2, col=1)

    # ── RSI ────────────────────────────────────────────────────────────────
    rsi_row = 3
    if has_rsi:
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist["RSI"],
            mode="lines", name="RSI",
            line=dict(color="#9C27B0", width=1.5),
        ), row=rsi_row, col=1)
        fig.add_hline(y=70, line_dash="dot", line_color="red",   row=rsi_row, col=1)
        fig.add_hline(y=30, line_dash="dot", line_color="green", row=rsi_row, col=1)
        fig.update_yaxes(range=[0, 100], row=rsi_row, col=1)

    # ── MACD ───────────────────────────────────────────────────────────────
    macd_row = rsi_row + (1 if has_rsi else 0)
    if has_macd:
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist["MACD"],
            mode="lines", name="MACD",
            line=dict(color="#00BCD4", width=1.5),
        ), row=macd_row, col=1)
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist["MACD_signal"],
            mode="lines", name="Signal",
            line=dict(color="#FF5722", width=1, dash="dash"),
        ), row=macd_row, col=1)
        hist["MACD_hist"] = hist["MACD"] - hist["MACD_signal"]
        fig.add_trace(go.Bar(
            x=hist.index, y=hist["MACD_hist"],
            name="Histogramme",
            marker_color=hist["MACD_hist"].apply(
                lambda v: "#26a69a" if v >= 0 else "#ef5350"
            ),
        ), row=macd_row, col=1)

    # ── Mise en forme globale ──────────────────────────────────────────────
    fig.update_layout(
        template="plotly_dark",
        height=200 + 130 * rows,
        margin=dict(l=50, r=20, t=40, b=20),
        legend=dict(orientation="h", y=1.02, x=0),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)")

    return fig
```

---

## C. Interface — désactiver les options sans données

### Dans le layout Dash (partie callback ou layout)
```python
# Avant
dcc.Checklist(id="indicators", options=[
    {"label": "RSI",        "value": "rsi"},
    {"label": "MACD",       "value": "macd"},
    {"label": "Bollinger",  "value": "bb"},
])

# Après — désactiver dynamiquement selon la longueur de l'historique
@app.callback(
    Output("indicators", "options"),
    Input("period-selector", "value"),
    Input("ticker-input", "value"),
)
def update_indicator_options(period_label, ticker_symbol):
    base_options = [
        {"label": "RSI",       "value": "rsi"},
        {"label": "MACD",      "value": "macd"},
        {"label": "Bollinger", "value": "bb"},
    ]
    try:
        t    = yf.Ticker(ticker_symbol)
        hist = get_history(t, period_label)
        enough = len(hist) >= 14
    except Exception:
        enough = False

    return [
        {**opt, "disabled": not enough}
        for opt in base_options
    ]
```

### Ajouter un message d'avertissement pour 1J
```python
@app.callback(
    Output("period-warning", "children"),
    Input("period-selector", "value"),
)
def period_warning(period_label):
    if period_label == "1J":
        return "⚠️ Mode intraday (5 min) — les bougies peuvent être incomplètes en dehors des heures de marché."
    return ""
```

```python
# Dans le layout
html.Div(id="period-warning", style={"color": "#FF9800", "fontSize": "0.85rem", "marginTop": "4px"}),
```

---

## D. Sélecteur de type de graphique

```python
# Dans le layout
dcc.RadioItems(
    id="chart-type",
    options=[
        {"label": "🕯️ Candlestick", "value": "Candlestick"},
        {"label": "📈 Line",        "value": "Line"},
        {"label": "🌊 Area",        "value": "Area"},
    ],
    value="Candlestick",
    inline=True,
    style={"marginBottom": "8px"},
),

# Dans le callback principal
@app.callback(
    Output("chart", "figure"),
    Input("ticker-input",    "value"),
    Input("period-selector", "value"),
    Input("indicators",      "value"),
    Input("chart-type",      "value"),
)
def update_chart(ticker_symbol, period_label, indicators, chart_type):
    indicators = indicators or []
    t    = yf.Ticker(ticker_symbol)
    hist = get_history(t, period_label)

    return build_chart(
        hist,
        show_rsi  = "rsi"  in indicators,
        show_macd = "macd" in indicators,
        show_bb   = "bb"   in indicators,
        chart_type= chart_type,
    )
```

---

## E. Améliorer la comparaison de tickers

### Avant
```python
def compare_tickers(t1, t2, period):
    h1 = t1.history(period=period)["Close"]
    h2 = t2.history(period=period)["Close"]
    norm1 = h1 / h1.iloc[0] * 100
    norm2 = h2 / h2.iloc[0] * 100
    ...
```

### Après
```python
def compare_tickers(symbol1, symbol2, period_label="1M"):
    cfg = PERIOD_CONFIG.get(period_label, {"period": "1mo", "interval": "1d"})

    h1 = yf.Ticker(symbol1).history(**cfg)[["Close", "Volume"]]
    h2 = yf.Ticker(symbol2).history(**cfg)[["Close", "Volume"]]

    # Aligner les index (dates communes uniquement)
    h1, h2 = h1.align(h2, join="inner")

    if h1.empty:
        return go.Figure().update_layout(title="Aucune date commune trouvée")

    # Performance relative (%)
    perf1 = (h1["Close"] / h1["Close"].iloc[0] - 1) * 100
    perf2 = (h2["Close"] / h2["Close"].iloc[0] - 1) * 100

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.7, 0.3],
                        subplot_titles=["Performance (%)", "Volume"])

    fig.add_trace(go.Scatter(x=perf1.index, y=perf1, name=symbol1,
                             line=dict(color="#2196F3", width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=perf2.index, y=perf2, name=symbol2,
                             line=dict(color="#FF9800", width=1.5)), row=1, col=1)
    fig.add_hline(y=0, line_dash="dot", line_color="gray", row=1, col=1)

    fig.add_trace(go.Bar(x=h1.index, y=h1["Volume"], name=f"Vol {symbol1}",
                         marker_color="rgba(33,150,243,0.5)"), row=2, col=1)
    fig.add_trace(go.Bar(x=h2.index, y=h2["Volume"], name=f"Vol {symbol2}",
                         marker_color="rgba(255,152,0,0.5)"), row=2, col=1)

    fig.update_layout(template="plotly_dark", hovermode="x unified",
                      margin=dict(l=50, r=20, t=40, b=20))
    return fig
```

---

## Résumé des modifications

| # | Fichier | Section | Impact |
|---|---------|---------|--------|
| A | `dashboard.py` | `get_history()` | Fix intraday `1J`, intervalles adaptés par période |
| B | `dashboard.py` | `build_chart()` | Sous-graphes séparés, volume, couleurs up/down |
| C | `dashboard.py` | Callback layout | Options désactivées si données insuffisantes |
| D | `dashboard.py` | Layout + callback | Sélecteur Candlestick / Line / Area |
| E | `dashboard.py` | `compare_tickers()` | Alignement des dates, performance %, volumes |