import os
import yfinance as yf
import psycopg2
from datetime import datetime
from psycopg2.extras import execute_values

# Get DB URL from GitHub secret
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL not found in environment variables.")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

try:
    # Fetch symbols dynamically
    cursor.execute("SELECT symbol FROM stock_symbols;")
    symbols = [row[0] for row in cursor.fetchall()]

    print(f"Fetching data for {len(symbols)} symbols...")

    insert_data = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")

            if data.empty:
                print(f"No data returned for {symbol}")
                continue

            latest_row = data.tail(1)
            latest_price = float(latest_row["Close"].iloc[-1])
            market_timestamp = latest_row.index[-1].to_pydatetime()

            insert_data.append((symbol, latest_price, market_timestamp))

            print(f"{symbol} | {latest_price} | {market_timestamp}")

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    if insert_data:
        execute_values(
            cursor,
            """
            INSERT INTO stock_prices (symbol, price, timestamp)
            VALUES %s
            ON CONFLICT (symbol, timestamp) DO NOTHING;
            """,
            insert_data
        )

        conn.commit()
        print("Stock prices inserted successfully.")

    else:
        print("No new data to insert.")

except Exception as main_error:
    print("Pipeline failed:", main_error)

finally:
    cursor.close()
    conn.close()