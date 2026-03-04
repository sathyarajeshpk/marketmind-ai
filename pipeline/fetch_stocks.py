import os
import yfinance as yf
import psycopg2
from psycopg2.extras import execute_values

# Get DB URL from GitHub secret
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL not found in environment variables.")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

try:
    # Fetch stock symbols dynamically
    cursor.execute("SELECT symbol FROM stock_symbols;")
    symbols = [row[0] for row in cursor.fetchall()]

    print(f"Fetching data for {len(symbols)} symbols...")

    insert_data = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)

            # Fetch today's 1 minute candles
            data = ticker.history(period="1d", interval="1m")

            if data.empty:
                print(f"No data returned for {symbol}")
                continue

            # Only take last few minutes to reduce duplicates
            recent_rows = data.tail(10)

            for ts, row in recent_rows.iterrows():

                price = float(row["Close"])
                market_timestamp = ts.to_pydatetime()

                insert_data.append((symbol, price, market_timestamp))

            print(f"{symbol} -> collected {len(recent_rows)} rows")

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    if insert_data:
        execute_values(
            cursor,
            """
            INSERT INTO stock_prices (symbol, price, timestamp)
            VALUES %s
            ON CONFLICT (symbol, timestamp) DO NOTHING
            """,
            insert_data
        )

        conn.commit()
        print(f"{len(insert_data)} price records inserted.")

    else:
        print("No new market data.")

except Exception as main_error:
    print("Pipeline failed:", main_error)

finally:
    cursor.close()
    conn.close()

print("Stock pipeline finished.")