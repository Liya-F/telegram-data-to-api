import os
import json
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER,
    password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cur = conn.cursor()

# Ensure the raw schema exists
cur.execute("CREATE SCHEMA IF NOT EXISTS raw")

# Create table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS raw.raw_telegram_messages (
        id SERIAL PRIMARY KEY,
        message_id INTEGER,
        channel_name TEXT,
        message_text TEXT,
        message_date TIMESTAMP,
        views INTEGER,
        forwards INTEGER,
        has_media BOOLEAN,
        media_type TEXT,
        reply_count INTEGER,
        reactions_json TEXT
    )
""")
conn.commit()

# Load files from the data lake folder
data_path = "data/raw/telegram_messages"
today = "2025-07-15" 
folder = os.path.join(data_path, today)

for filename in os.listdir(folder):
    if not filename.endswith(".json"):
        continue

    channel_name = filename.replace(".json", "")
    with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
        messages = json.load(f)

    for msg in messages:
        message_id = msg.get("id")
        message_text = msg.get("message") or ""
        message_date = msg.get("date")
        views = msg.get("views") or 0
        forwards = msg.get("forwards") or 0

        has_media = msg.get("media") is not None
        media_type = msg.get("media", {}).get("_") if has_media else None

        replies_obj = msg.get("replies")
        reply_count = replies_obj.get("replies", None) if isinstance(replies_obj, dict) else None

        reactions_obj = msg.get("reactions")
        if isinstance(reactions_obj, dict):
            reactions = reactions_obj.get("results", [])
        else:
            reactions = []

        reactions_str = json.dumps(reactions, ensure_ascii=False)

        # Insert into the database
        cur.execute("""
            INSERT INTO raw.raw_telegram_messages (
                message_id, channel_name, message_text, message_date,
                views, forwards, has_media, media_type, reply_count, reactions_json
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            message_id, channel_name, message_text, message_date,
            views, forwards, has_media, media_type, reply_count, reactions_str
        ))

conn.commit()
cur.close()
conn.close()
print("✅ Data successfully loaded into PostgreSQL.")
