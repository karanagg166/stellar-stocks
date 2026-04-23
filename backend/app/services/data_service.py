"""
Data Service — Fetches stock data from Yahoo Finance via yfinance,
cleans it with Pandas, and returns structured DataFrames.
"""

import yfinance as yf
import pandas as pd
import numpy as np

# Companies to fetch — 10 major NSE-listed Indian stocks
COMPANIES = {
    "RELIANCE.NS": {"name": "Reliance Industries", "sector": "Energy"},
    "TCS.NS": {"name": "Tata Consultancy Services", "sector": "IT"},
    "INFY.NS": {"name": "Infosys", "sector": "IT"},
    "HDFCBANK.NS": {"name": "HDFC Bank", "sector": "Banking"},
    "ICICIBANK.NS": {"name": "ICICI Bank", "sector": "Banking"},
    "HINDUNILVR.NS": {"name": "Hindustan Unilever", "sector": "FMCG"},
    "SBIN.NS": {"name": "State Bank of India", "sector": "Banking"},
    "BHARTIARTL.NS": {"name": "Bharti Airtel", "sector": "Telecom"},
    "ITC.NS": {"name": "ITC", "sector": "FMCG"},
    "WIPRO.NS": {"name": "Wipro", "sector": "IT"},
}


def fetch_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a given symbol from Yahoo Finance.

    Args:
        symbol: Stock ticker symbol (e.g., "RELIANCE.NS")
        period: Time period to fetch (default: "1y" for 1 year)

    Returns:
        Cleaned DataFrame with OHLCV data
    """
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)

    if df.empty:
        print(f"  ⚠️  No data returned for {symbol}")
        return pd.DataFrame()

    # Reset index to make Date a column
    df = df.reset_index()

    # Rename columns to snake_case
    df = df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    })

    # Keep only needed columns
    df = df[["date", "open", "high", "low", "close", "volume"]]

    # Clean date — remove timezone info, convert to date only
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None).dt.date

    # Handle missing values
    df = df.dropna(subset=["open", "high", "low", "close"])
    df["volume"] = df["volume"].fillna(0).astype(int)

    # Remove any duplicate dates
    df = df.drop_duplicates(subset=["date"], keep="last")

    # Sort by date ascending
    df = df.sort_values("date").reset_index(drop=True)

    return df


def add_calculated_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add calculated metrics to the stock DataFrame.

    Metrics added:
    - daily_return: (close - open) / open
    - moving_avg_7d: 7-day rolling mean of close
    - high_52w: Rolling 252-day (52 weeks) max of high
    - low_52w: Rolling 252-day (52 weeks) min of low
    - volatility_score: Annualized 20-day rolling std of daily returns
    """
    if df.empty:
        return df

    # Daily Return = (Close - Open) / Open
    df["daily_return"] = ((df["close"] - df["open"]) / df["open"]).round(6)

    # 7-day Moving Average of Close
    df["moving_avg_7d"] = df["close"].rolling(window=7, min_periods=1).mean().round(2)

    # 52-week High (using available data, max 252 trading days)
    df["high_52w"] = df["high"].rolling(window=252, min_periods=1).max().round(2)

    # 52-week Low
    df["low_52w"] = df["low"].rolling(window=252, min_periods=1).min().round(2)

    # Volatility Score — Annualized 20-day rolling standard deviation of daily returns
    # Annualized by multiplying by sqrt(252)
    pct_change = df["close"].pct_change()
    rolling_std = pct_change.rolling(window=20, min_periods=5).std()
    df["volatility_score"] = (rolling_std * np.sqrt(252)).round(4)

    # Replace NaN/inf with None for clean DB storage
    df = df.replace([np.inf, -np.inf], np.nan)

    return df


def fetch_and_prepare(symbol: str) -> pd.DataFrame:
    """Fetch stock data and add all calculated metrics."""
    df = fetch_stock_data(symbol)
    if df.empty:
        return df
    return add_calculated_metrics(df)
