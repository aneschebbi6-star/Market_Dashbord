import os
import yfinance as yf
import pandas as pd
try:
    import ta
except Exception:
    ta = None
import requests
try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import nltk
except Exception:
    SentimentIntensityAnalyzer = None
    nltk = None

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if nltk is not None:
    # Download VADER lexicon for sentiment analysis if missing
    try:
        nltk.data.find('sentiment/vader_lexicon')
    except LookupError:
        try:
            nltk.download('vader_lexicon', quiet=True)
        except Exception:
            pass


def get_prices(symbols=["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "GC=F", "SI=F", "CL=F"]):
    data_output = {}
    
    for symbol in symbols:
        try:
            # Récupérer les infos du jour
            t = yf.Ticker(symbol)
            hist = t.history(period="2d")
            
            if symbol.upper() == "GC=F":
                name = "gold"
            elif symbol.upper() == "SI=F":
                name = "silver"
            elif symbol.upper() == "CL=F":
                name = "oil"
            else:
                name = symbol.replace("-USD", "").lower()
            
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change = ((current_price - prev_price) / prev_price) * 100
                
                data_output[name] = {
                    "usd": current_price,
                    "usd_24h_change": change,
                    "symbol": symbol
                }
            elif not hist.empty:
                data_output[name] = {
                    "usd": hist['Close'].iloc[-1],
                    "usd_24h_change": 0,
                    "symbol": symbol
                }
        except Exception as e:
            print(f"Erreur pour {symbol}: {e}")
            
    return data_output

PERIOD_CONFIG = {
    "1J": {"period": "1d",  "interval": "5m"},
    "7J": {"period": "7d",  "interval": "1h"},
    "1M": {"period": "1mo", "interval": "1d"},
    "3M": {"period": "3mo", "interval": "1d"},
    "1A": {"period": "1y",  "interval": "1d"},
    "5A": {"period": "5y",  "interval": "1wk"},
}


def get_history(ticker_or_name="bitcoin", period_label="1M"):
    # Dictionnaire de secours pour les noms communs vers tickers
    mapping = {
        "bitcoin": "BTC-USD",
        "ethereum": "ETH-USD",
        "solana": "SOL-USD",
        "gold": "GC=F",
        "silver": "SI=F",
        "oil": "CL=F",
        "wti": "CL=F",
        "crude oil": "CL=F",
        "xau": "GC=F",
        "xag": "SI=F"
    }

    period_label_map = {
        1: "1J",
        7: "7J",
        30: "1M",
        90: "3M",
        365: "1A",
    }

    # Support older numeric days values pour compatibilité
    if isinstance(period_label, int):
        period_label = period_label_map.get(period_label, "1M")
    elif isinstance(period_label, str) and period_label.isdigit():
        period_label = period_label_map.get(int(period_label), "1M")

    ticker = mapping.get(ticker_or_name.lower(), ticker_or_name)

    # S'assurer que le ticker est bien formaté pour YahooFinance
    if "-" not in ticker and "=" not in ticker:
        ticker = ticker.upper() + "-USD"
    else:
        ticker = ticker.upper()

    cfg = PERIOD_CONFIG.get(period_label, {"period": "1mo", "interval": "1d"})

    # Commodity tickers that trade on specific exchanges with limited intraday hours
    COMMODITY_TICKERS = {"GC=F", "SI=F", "CL=F"}

    try:
        t = yf.Ticker(ticker)
        used_interval = cfg["interval"]
        hist = t.history(period=cfg["period"], interval=used_interval)

        # If no data or very few bars (common for commodities at fine resolution),
        # try coarser intraday intervals as a fallback so charts aren't empty.
        if hist.empty or len(hist) < 5:
            if ticker in COMMODITY_TICKERS:
                alt_intervals = [
                    # coarser to finer — prefer hourly/30m for CME-traded commodities
                    "1h",
                    "30m",
                    "15m",
                ]
                for alt in alt_intervals:
                    try:
                        hist = t.history(period=cfg["period"], interval=alt)
                        if not hist.empty and len(hist) >= 5:
                            used_interval = alt
                            print(f"Fetched commodity data for {ticker} with interval={alt}")
                            break
                    except Exception:
                        continue

        if hist.empty:
            return hist

        hist = hist.dropna(how="all")

        # Calculer les indicateurs techniques si la librairie 'ta' est disponible
        if ta is not None:
            if len(hist) >= 14:
                try:
                    hist['RSI'] = ta.momentum.RSIIndicator(hist['Close'], window=14).rsi()
                except Exception:
                    pass

                try:
                    macd = ta.trend.MACD(hist['Close'])
                    hist['MACD'] = macd.macd()
                    hist['MACD_Signal'] = macd.macd_signal()
                    hist['MACD_Diff'] = macd.macd_diff()
                    hist['MACD_Hist'] = hist['MACD'] - hist['MACD_Signal']
                except Exception:
                    pass

            if len(hist) >= 20:
                try:
                    bb = ta.volatility.BollingerBands(hist['Close'], window=20, window_dev=2)
                    hist['BB_High'] = bb.bollinger_hband()
                    hist['BB_Low'] = bb.bollinger_lband()
                    hist['BB_Mid'] = bb.bollinger_mavg()
                except Exception:
                    pass

        # Compute moving averages in a timeframe-aware way.
        # For intraday intervals, a 'MA50' should represent 50 days, not 50 bars.
        interval = cfg.get("interval", "1d")

        bars_per_day_map = {
            "1m": 1440,
            "5m": 288,
            "15m": 96,
            "30m": 48,
            "1h": 24,
            "4h": 6,
            "1d": 1,
            "1wk": 1,
        }

        bpd = bars_per_day_map.get(interval, 1)
        window50 = int(50 * bpd)
        window200 = int(200 * bpd)

        # If we have enough bars to compute day-equivalent MAs, do rolling on that window.
        # Otherwise, avoid misleading short-window rolling averages and provide an EMA fallback.
        if len(hist) >= window50 and window50 > 1:
            hist['MA50'] = hist['Close'].rolling(window=window50).mean()
        elif interval == '1d' and len(hist) >= 50:
            hist['MA50'] = hist['Close'].rolling(window=50).mean()
        else:
            hist['MA50'] = pd.NA

        if len(hist) >= window200 and window200 > 1:
            hist['MA200'] = hist['Close'].rolling(window=window200).mean()
        elif interval == '1d' and len(hist) >= 200:
            hist['MA200'] = hist['Close'].rolling(window=200).mean()
        else:
            hist['MA200'] = pd.NA

        # Provide a sensible intraday alternative: a shorter EMA that is meaningful on the
        # displayed timeframe (e.g., EMA20) so traders still see a smoothed reference.
        hist['EMA20'] = hist['Close'].ewm(span=20, adjust=False).mean()

        # Store metadata about the interval actually used so the UI can explain fallbacks
        try:
            hist.attrs['interval_used'] = used_interval
        except Exception:
            pass

        return hist
    except Exception as e:
        print(f"Erreur historique pour {ticker}: {e}")
        return pd.DataFrame()

def get_news(query, limit=10):
    """Fetch news articles for `query` using NewsAPI.org if configured.

    Returns a list of article dicts with at least 'title' and 'url'.
    If no API key or on error, returns an empty list.
    """
    api_key = os.environ.get('NEWSAPI_KEY')
    if not api_key:
        return []

    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'apiKey': api_key,
        'pageSize': min(100, limit),
        'language': 'en',
        'sortBy': 'relevancy'
    }
    try:
        resp = requests.get(url, params=params, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get('articles', [])[:limit]
        # Normalize to minimal fields expected by UI
        normalized = []
        for a in articles:
            normalized.append({'title': a.get('title', ''), 'url': a.get('url', ''), 'source': a.get('source', {}).get('name')})
        return normalized
    except Exception:
        return []


import re

CRYPTO_LEXICON = {
    # Bullish slang
    "moon": 3.0,
    "mooning": 3.5,
    "hodl": 2.0,
    "hodling": 2.0,
    "bullish": 3.0,
    "pump": 2.0,
    "pumping": 2.5,
    "rally": 2.0,
    "rallying": 2.0,
    "ath": 2.5,          # all-time high
    "accumulate": 1.5,
    "accumulating": 1.5,
    "breakout": 2.0,
    "undervalued": 1.5,
    "adoption": 1.5,
    "bullrun": 3.0,

    # Bearish slang
    "bearish": -3.0,
    "dump": -2.5,
    "dumping": -2.5,
    "dumps": -2.5,
    "rekt": -3.5,
    "fud": -2.0,
    "capitulation": -3.0,
    "liquidated": -3.0,
    "liquidation": -2.5,
    "crash": -3.0,
    "crashing": -3.0,
    "correction": -1.0,
    "selloff": -2.0,
    "bearmarket": -2.5,
    "scam": -3.5,
    "hack": -3.0,
    "hacked": -3.5,
    "exploit": -2.5,
    "exploited": -3.0,
    "overvalued": -1.5,

    # Neutral-ish but domain-relevant (kept mild so they don't skew scores)
    "fomo": 0.5,
    "whale": 0.0,
    "airdrop": 1.0,
}

# Multi-word phrases VADER can't score as a single unit by default.
# We normalize them into single tokens *before* running the analyzer,
# then score those tokens via CRYPTO_LEXICON.
PHRASE_REPLACEMENTS = {
    r"\bto the moon\b": "cryptophrase_extremely_bullish",
    r"\brug pull\b": "cryptophrase_extremely_bearish",
    r"\brug[- ]?pulled\b": "cryptophrase_extremely_bearish",
    r"\bdiamond hands?\b": "cryptophrase_very_bullish",
    r"\bpaper hands?\b": "cryptophrase_bearish",
    r"\bshort squeeze\b": "cryptophrase_bullish",
    r"\bdeath cross\b": "cryptophrase_bearish",
    r"\bgolden cross\b": "cryptophrase_bullish",
    r"\ball[- ]time high\b": "cryptophrase_bullish",
    r"\ball[- ]time low\b": "cryptophrase_bearish",
}

PHRASE_LEXICON = {
    "cryptophrase_extremely_bullish": 3.5,
    "cryptophrase_extremely_bearish": -3.5,
    "cryptophrase_very_bullish": 2.5,
    "cryptophrase_bearish": -1.5,
    "cryptophrase_bullish": 2.0,
}

_crypto_analyzer = None  # cached singleton, built once


def get_crypto_analyzer():
    """Return a VADER analyzer extended with crypto-domain vocabulary.

    Built once and cached, since constructing SentimentIntensityAnalyzer()
    and updating its lexicon on every call is wasteful.
    """
    global _crypto_analyzer
    if _crypto_analyzer is None:
        if SentimentIntensityAnalyzer is None:
            # Fallback lightweight analyzer that returns neutral scores when nltk isn't installed
            class _FallbackAnalyzer:
                def polarity_scores(self, _text):
                    return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}

            _crypto_analyzer = _FallbackAnalyzer()
        else:
            analyzer = SentimentIntensityAnalyzer()
            analyzer.lexicon.update(CRYPTO_LEXICON)
            analyzer.lexicon.update(PHRASE_LEXICON)
            _crypto_analyzer = analyzer
    return _crypto_analyzer


def preprocess_crypto_text(text):
    """Normalize crypto multi-word phrases into single scorable tokens."""
    normalized = text.lower()
    for pattern, replacement in PHRASE_REPLACEMENTS.items():
        normalized = re.sub(pattern, replacement, normalized)
    return normalized


def analyze_sentiment(headlines):
    """Analyze sentiment of headlines using VADER + a crypto-domain lexicon.

    Args:
        headlines: List of article dictionaries with 'title' key

    Returns:
        Dictionary with:
        - 'score': Average sentiment score (-1 to 1)
        - 'label': 'Bearish', 'Neutral', or 'Bullish'
        - 'articles': List of articles with sentiment scores
    """
    analyzer = get_crypto_analyzer()

    if not headlines:
        return {'score': 0, 'label': 'Neutral', 'articles': []}

    sentiments = []
    articles_with_sentiment = []

    for article in headlines:
        title = article.get('title', '')
        normalized_title = preprocess_crypto_text(title)
        scores = analyzer.polarity_scores(normalized_title)
        compound_score = scores['compound']  # -1 to 1

        sentiments.append(compound_score)

        article_data = article.copy()
        article_data['sentiment_score'] = compound_score

        # Classify sentiment
        if compound_score >= 0.05:
            article_data['sentiment_label'] = 'Bullish'
            article_data['color'] = 'green'
        elif compound_score <= -0.05:
            article_data['sentiment_label'] = 'Bearish'
            article_data['color'] = 'red'
        else:
            article_data['sentiment_label'] = 'Neutral'
            article_data['color'] = 'gray'

        articles_with_sentiment.append(article_data)

    # Calculate average sentiment
    avg_sentiment = sum(sentiments) / len(sentiments)

    # Classify overall sentiment
    if avg_sentiment >= 0.1:
        label = 'Bullish'
    elif avg_sentiment <= -0.1:
        label = 'Bearish'
    else:
        label = 'Neutral'

    return {
        'score': avg_sentiment,
        'label': label,
        'articles': articles_with_sentiment
    }