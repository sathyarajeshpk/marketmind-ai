import os
import yfinance as yf
import psycopg2
import pandas as pd
from datetime import datetime

# Get DB URL from GitHub secret
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Fetch symbols dynamically
cursor.execute("SELECT symbol FROM stock_symbols;")
symbols = [row[0] for row in cursor.fetchall()]

for symbol in symbols:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m").tail(1)

    if not data.empty:
        latest_price = float(data["Close"].iloc[-1])

        cursor.execute("""
            INSERT INTO stock_prices (symbol, price, timestamp)
            VALUES (%s, %s, %s)
        """, (symbol, latest_price, datetime.now()))

conn.commit()
cursor.close()
conn.close()

print("Stock prices updated successfully.")