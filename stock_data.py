# stock_data.py
import yfinance as yf
import pandas as pd

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        history = stock.history(period="1mo")

        current_price = history['Close'].iloc[-1]
        price_30d_ago = history['Close'].iloc[0]
        change_30d = ((current_price - price_30d_ago) / price_30d_ago * 100)
        avg_volume = history['Volume'].tail(7).mean()

        return {
            "symbol": symbol,
            "company_name": info.get('longName', symbol),
            "current_price": round(current_price, 2),
            "change_30d_percent": round(change_30d, 2),
            "52_week_high": info.get('fiftyTwoWeekHigh', 'N/A'),
            "52_week_low": info.get('fiftyTwoWeekLow', 'N/A'),
            "market_cap": info.get('marketCap', 'N/A'),
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "avg_volume_7d": round(avg_volume, 0),
            "history": history
        }

    except Exception as e:
        return {"error": str(e)}