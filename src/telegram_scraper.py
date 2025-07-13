import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError, ChannelPrivateError
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE") 

client = TelegramClient('session', api_id, api_hash)

channels = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
    "https://t.me/CheMed123"
]


today_str = datetime.today().strftime("%Y-%m-%d")
log_file = "scrape_log.txt"

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} - {msg}\n")

with client:
    for url in channels:
        try:
            entity = client.get_entity(url)
            channel_name = entity.username or str(entity.id)
            messages = [msg.to_dict() for msg in client.iter_messages(entity, limit=100)]

            save_path = f"data/raw/telegram_messages/{today_str}/{channel_name}.json"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2, default=str)

            log(f"✅ Scraped {len(messages)} messages from {url} → {save_path}")

        except ChannelPrivateError:
            log(f"❌ Skipped private/inaccessible channel: {url}")
        except FloodWaitError as e:
            log(f"⚠️ Rate limited! Wait {e.seconds} seconds before retrying.")
        except Exception as e:
            log(f"❌ Failed to scrape {url} due to {type(e).__name__}: {e}")
