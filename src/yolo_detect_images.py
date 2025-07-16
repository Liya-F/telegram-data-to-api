import os
from ultralytics import YOLO
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Load DB config
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Create table for image detections
cur.execute("""
CREATE TABLE IF NOT EXISTS raw.image_detections (
    id SERIAL PRIMARY KEY,
    channel_name TEXT,
    image_file TEXT,
    detected_class TEXT,
    confidence_score FLOAT
);
""")
conn.commit()

# Load YOLOv8 model (nano version for speed)
model = YOLO("yolov8n.pt")

# Define the image directory (adjust date if needed)
image_root = "data/raw/images/2025-07-13"

total_detections = 0
skipped = 0
errors = 0

# Iterate over each channel folder
for channel in os.listdir(image_root):
    channel_path = os.path.join(image_root, channel)
    if not os.path.isdir(channel_path):
        continue

    for image_file in os.listdir(channel_path):
        if not image_file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        image_path = os.path.join(channel_path, image_file)

        try:
            if os.path.getsize(image_path) == 0:
                print(f"⚠️ Skipped empty image: {image_file}")
                skipped += 1
                continue

            results = model(image_path, verbose=False)[0]

            for box in results.boxes:
                cls = results.names[int(box.cls[0])]
                conf = float(box.conf[0])

                cur.execute("""
                    INSERT INTO raw.image_detections (
                        channel_name, image_file, detected_class, confidence_score
                    ) VALUES (%s, %s, %s, %s)
                """, (channel, image_file, cls, conf))
                total_detections += 1

        except Exception as e:
            print(f"❌ Error processing {image_file}: {type(e).__name__} - {e}")
            errors += 1
            continue

conn.commit()
cur.close()
conn.close()

print(f"\n✅ YOLOv8 complete")
print(f"   ✔️ Total objects detected: {total_detections}")
print(f"   ⚠️ Skipped empty files: {skipped}")
print(f"   ❌ Files with errors: {errors}")
