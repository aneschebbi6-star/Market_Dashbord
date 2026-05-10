import yfinance as yf
import pandas as pd
import ta

def get_prices(symbols=["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "ADA-USD", "DOGE-USD"]):
    data_output = {}
    
    for symbol in symbols:
        try:
            # Récupérer les infos du jour
            t = yf.Ticker(symbol)
            hist = t.history(period="2d")
            
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

def get_history(ticker_or_name="bitcoin", days=7):
    # Dictionnaire de secours pour les noms communs vers tickers
    mapping = {
        "bitcoin": "BTC-USD",
        "ethereum": "ETH-USD",
        "solana": "SOL-USD"
    }
    
    ticker = mapping.get(ticker_or_name.lower(), ticker_or_name)
    
    # S'assurer que le ticker finit par -USD s'il n'a pas de tiret
    if "-" not in ticker:
        ticker = ticker.upper() + "-USD"
    
    period = f"{days}d"
    
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period)
        
        # Calculer les indicateurs techniques
        if not hist.empty and len(hist) > 14: # On s'assure d'avoir assez de données pour l'indicateur
            # RSI (Relative Strength Index)
            hist['RSI'] = ta.momentum.RSIIndicator(hist['Close'], window=14).rsi()
            
            # MACD
            macd = ta.trend.MACD(hist['Close'])
            hist['MACD'] = macd.macd()
            hist['MACD_Signal'] = macd.macd_signal()
            hist['MACD_Diff'] = macd.macd_diff()
            
            # Bandes de Bollinger
            bb = ta.volatility.BollingerBands(hist['Close'], window=20, window_dev=2)
            hist['BB_High'] = bb.bollinger_hband()
            hist['BB_Low'] = bb.bollinger_lband()
            hist['BB_Mid'] = bb.bollinger_mavg()
            
        return hist
    except Exception as e:
        print(f"Erreur historique pour {ticker}: {e}")
        return pd.DataFrame()