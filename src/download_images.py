import os
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient('session', api_id, api_hash)

# Channels to download images from
channels = [
    #"https://t.me/lobelia4cosmetics",
    #"https://t.me/tikvahpharma",
    "https://t.me/CheMed123",
]

today_str = datetime.today().strftime("%Y-%m-%d")

with client:
    for url in channels:
        try:
            entity = client.get_entity(url)
            channel_name = entity.username or str(entity.id)
            save_dir = f"data/raw/images/{today_str}/{channel_name}"
            os.makedirs(save_dir, exist_ok=True)

            print(f"📥 Downloading images from {channel_name}...")

            count = 0
            for msg in client.iter_messages(entity, limit=200):
                if msg.media and isinstance(msg.media, MessageMediaPhoto):
                    count += 1
                    file_path = os.path.join(save_dir, f"image_{count:04d}.jpg")
                    client.download_media(msg, file_path)

            print(f"✅ Downloaded {count} images from {channel_name}")

        except Exception as e:
            print(f"❌ Error with {url}: {e}")
