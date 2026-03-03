import os
import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Get all symbols
cursor.execute("SELECT DISTINCT symbol FROM stock_prices;")
symbols = [row[0] for row in cursor.fetchall()]

for symbol in symbols:

    query = """
        SELECT price, timestamp
        FROM stock_prices
        WHERE symbol = %s
        ORDER BY timestamp ASC
    """

    df = pd.read_sql(query, conn, params=(symbol,))

    if len(df) < 20:
        continue  # Need minimum data

    df["ma_20"] = df["price"].rolling(window=20).mean()
    df["ma_50"] = df["price"].rolling(window=50).mean()
    df["daily_return"] = df["price"].pct_change()
    df["volatility"] = df["daily_return"].rolling(window=20).std()

    latest = df.iloc[-1]

    # Signal logic
    if latest["price"] > latest["ma_20"] and latest["price"] > latest["ma_50"]:
        signal = "Bullish"
    elif latest["price"] < latest["ma_20"] and latest["price"] < latest["ma_50"]:
        signal = "Bearish"
    else:
        signal = "Neutral"

    cursor.execute("""
        INSERT INTO stock_metrics
        (symbol, ma_20, ma_50, daily_return, volatility, signal, calculated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        symbol,
        float(latest["ma_20"]) if not np.isnan(latest["ma_20"]) else None,
        float(latest["ma_50"]) if not np.isnan(latest["ma_50"]) else None,
        float(latest["daily_return"]) if not np.isnan(latest["daily_return"]) else None,
        float(latest["volatility"]) if not np.isnan(latest["volatility"]) else None,
        signal,
        datetime.now()
    ))

conn.commit()
cursor.close()
conn.close()

print("Metrics calculated successfully.")