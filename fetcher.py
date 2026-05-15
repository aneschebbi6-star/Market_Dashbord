import os
import yfinance as yf
import pandas as pd
import ta
import requests
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Download VADER lexicon for sentiment analysis
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)


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

    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=cfg["period"], interval=cfg["interval"])
        
        if hist.empty:
            return hist

        hist = hist.dropna(how="all")

        # Calculer les indicateurs techniques
        if len(hist) >= 14:
            hist['RSI'] = ta.momentum.RSIIndicator(hist['Close'], window=14).rsi()
            
            macd = ta.trend.MACD(hist['Close'])
            hist['MACD'] = macd.macd()
            hist['MACD_Signal'] = macd.macd_signal()
            hist['MACD_Diff'] = macd.macd_diff()
            hist['MACD_Hist'] = hist['MACD'] - hist['MACD_Signal']

        if len(hist) >= 20:
            bb = ta.volatility.BollingerBands(hist['Close'], window=20, window_dev=2)
            hist['BB_High'] = bb.bollinger_hband()
            hist['BB_Low'] = bb.bollinger_lband()
            hist['BB_Mid'] = bb.bollinger_mavg()

        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        hist['MA200'] = hist['Close'].rolling(window=200).mean()

        return hist
    except Exception as e:
        print(f"Erreur historique pour {ticker}: {e}")
        return pd.DataFrame()


def get_news(crypto_name, limit=10):
    """Fetch latest real-time news for a cryptocurrency using NewsAPI.
    
    Args:
        crypto_name: Crypto name (e.g., 'bitcoin', 'ethereum')
        limit: Number of articles to fetch (default 10)
    
    Returns:
        List of dictionaries with keys: title, source, url, published_at
    """
    
    news_api_key = os.getenv("NEWSAPI_KEY")
    
    if not news_api_key:
        print("Warning: NEWSAPI_KEY not configured. Using demo data.")
        print("Get a free key at: https://newsapi.org/")
        return get_demo_news(crypto_name, limit)
    
    try:
        url = "https://newsapi.org/v2/everything"
        
        # Build search query
        crypto_queries = {
            "bitcoin": "Bitcoin BTC",
            "ethereum": "Ethereum ETH",
            "solana": "Solana SOL",
            "ripple": "XRP Ripple",
            "cardano": "Cardano ADA",
            "dogecoin": "Dogecoin DOGE",
            "binancecoin": "Binance BNB",
            "gold": "Gold XAU",
            "silver": "Silver XAG",
            "oil": "Crude Oil WTI"
        }
        
        query = crypto_queries.get(crypto_name.lower(), crypto_name)
        
        params = {
            "q": query,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": limit,
            "apiKey": news_api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == 'ok' and 'articles' in data:
            news_list = []
            for article in data['articles'][:limit]:
                news_list.append({
                    'title': article.get('title', 'N/A'),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'votes_positive': 0,
                    'votes_negative': 0
                })
            
            if news_list:
                print(f"✓ Real-time news loaded for {crypto_name} from NewsAPI")
                return news_list
        
        print(f"No articles found via NewsAPI for {crypto_name}")
        return get_demo_news(crypto_name, limit)
        
    except requests.exceptions.RequestException as e:
        print(f"NewsAPI error for {crypto_name}: {e}")
        return get_demo_news(crypto_name, limit)


def get_demo_news(crypto_name, limit=10):
    """Return demo news data as fallback.
    
    Args:
        crypto_name: Crypto name
        limit: Number of articles to return
    
    Returns:
        List of demo article dictionaries
    """
    DEMO_NEWS = {
        "bitcoin": [
            {"title": "Bitcoin Breaks $95K Resistance as Institutional Demand Surges", "source": "CryptoNews", "url": "https://cryptonews.com", "votes_positive": 2450, "votes_negative": 120},
            {"title": "BTC Rally Shows Signs of Sustainability According to On-Chain Analysts", "source": "Blockchain.com", "url": "https://blockchain.com", "votes_positive": 1890, "votes_negative": 245},
            {"title": "Federal Reserve Policy Impacts Bitcoin Price Movement This Week", "source": "Bitcoin Magazine", "url": "https://bitcoinmagazine.com", "votes_positive": 1560, "votes_negative": 890},
            {"title": "New Bitcoin ATM Rollout Expected in 500 Locations by Q2 2026", "source": "Coin Telegraph", "url": "https://cointelegraph.com", "votes_positive": 1240, "votes_negative": 350},
            {"title": "Bitcoin Network Reaches All-Time High in Transaction Value", "source": "CryptoSlate", "url": "https://cryptoslate.com", "votes_positive": 980, "votes_negative": 210},
        ],
        "ethereum": [
            {"title": "Ethereum Layer 2 Solutions See Record Adoption in May 2026", "source": "The Block", "url": "https://theblock.co", "votes_positive": 2100, "votes_negative": 340},
            {"title": "ETH Staking Rewards Hit New High, Pushing Capital Inflows", "source": "CryptoSlate", "url": "https://cryptoslate.com", "votes_positive": 1750, "votes_negative": 290},
            {"title": "Vitalik Buterin Announces Major Ethereum Protocol Improvement", "source": "Ethereum Foundation", "url": "https://ethereum.org", "votes_positive": 2650, "votes_negative": 180},
            {"title": "Ethereum Gas Fees Decline 25% Following Network Upgrade", "source": "DeFi Pulse", "url": "https://defipulse.com", "votes_positive": 1890, "votes_negative": 450},
            {"title": "Major Institutional Players Add ETH to Treasury", "source": "Bitcoin Magazine", "url": "https://bitcoinmagazine.com", "votes_positive": 1340, "votes_negative": 520},
        ],
        "solana": [
            {"title": "Solana Network Achieves Sub-Millisecond Finality", "source": "Solana Blog", "url": "https://solana.com", "votes_positive": 1650, "votes_negative": 420},
            {"title": "SOL Token Outperforms Market During Recent Volatility", "source": "CryptoNews", "url": "https://cryptonews.com", "votes_positive": 1240, "votes_negative": 380},
            {"title": "New DeFi Protocol Launch on Solana Breaks Records", "source": "DeFi Pulse", "url": "https://defipulse.com", "votes_positive": 980, "votes_negative": 210},
        ],
        "ripple": [
            {"title": "XRP Price Surge Amid Regulatory Clarity Announcement", "source": "Coin Telegraph", "url": "https://cointelegraph.com", "votes_positive": 1890, "votes_negative": 560},
            {"title": "Ripple Announces New Partnerships with Major Banks", "source": "The Block", "url": "https://theblock.co", "votes_positive": 2340, "votes_negative": 290},
        ],
    }
    
    demo_articles = DEMO_NEWS.get(crypto_name.lower(), [])
    return demo_articles[:limit] if demo_articles else []


def analyze_sentiment(headlines):
    """Analyze sentiment of headlines using VADER.
    
    Args:
        headlines: List of article dictionaries with 'title' key
    
    Returns:
        Dictionary with:
        - 'score': Average sentiment score (-1 to 1)
        - 'label': 'Bearish', 'Neutral', or 'Bullish'
        - 'articles': List of articles with sentiment scores
    """
    analyzer = SentimentIntensityAnalyzer()
    
    if not headlines:
        return {'score': 0, 'label': 'Neutral', 'articles': []}
    
    sentiments = []
    articles_with_sentiment = []
    
    for article in headlines:
        title = article.get('title', '')
        scores = analyzer.polarity_scores(title)
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
