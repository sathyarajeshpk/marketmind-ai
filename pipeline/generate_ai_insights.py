import os
import psycopg2
import requests
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")
HF_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Get latest metrics per stock
cursor.execute("""
    SELECT DISTINCT ON (symbol)
    symbol, ma_20, ma_50, daily_return, volatility, signal
    FROM stock_metrics
    ORDER BY symbol, calculated_at DESC
""")

rows = cursor.fetchall()

for row in rows:
    symbol, ma20, ma50, daily_return, volatility, signal = row

    prompt = f"""
    Stock: {symbol}
    MA20: {ma20}
    MA50: {ma50}
    Daily Return: {daily_return}
    Volatility: {volatility}
    Signal: {signal}

    Provide a short investment explanation under 120 words.
    Explain trend, risk level, and whether it looks suitable for long-term observation.
    """

    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 150}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, list):
        explanation = result[0]["generated_text"]
    else:
        explanation = "AI generation failed."

    cursor.execute("""
        INSERT INTO stock_ai_insights
        (symbol, explanation_text, generated_at)
        VALUES (%s, %s, %s)
    """, (symbol, explanation, datetime.now()))

conn.commit()
cursor.close()
conn.close()

print("AI insights generated successfully.")