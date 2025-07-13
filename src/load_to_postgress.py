import os
import json
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

PG_CONN = os.getenv("PG_CONN_STRING")  

conn = psycopg2.connect(PG_CONN)
cursor = conn.cursor()

# Create table if not exists (run only once ideally)
cursor.execute("""
CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    id BIGINT PRIMARY KEY,
    channel TEXT,
    text TEXT,
    date TIMESTAMP,
    has_media BOOLEAN,
    json_data JSONB
);
""")
conn.commit()

# Load all JSON files from folder
data_folder = "data/raw/telegram_messages"
for root, _, files in os.walk(data_folder):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                messages = json.load(f)
                for msg in messages:
                    msg_id = msg.get("id")
                    date = msg.get("date")
                    text = msg.get("message")
                    channel = msg.get("peer_id", {}).get("channel_id", "unknown")
                    has_media = msg.get("media") is not None

                    cursor.execute("""
                    INSERT INTO raw.telegram_messages (id, channel, text, date, has_media, json_data)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                    """, (msg_id, str(channel), text, date, has_media, json.dumps(msg)))
conn.commit()
cursor.close()
conn.close()
