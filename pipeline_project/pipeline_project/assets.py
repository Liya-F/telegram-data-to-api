from dagster import asset
import subprocess

@asset
def scrape_telegram_data():
    subprocess.run(["python", "src/telegram_scraper.py"], check=True)

@asset
def load_raw_to_postgres(scrape_telegram_data):
    subprocess.run(["python", "src/load_to_postgres.py"], check=True)

@asset
def run_dbt_transformations(load_raw_to_postgres):
    subprocess.run(["dbt", "run", "--project-dir", "telegram_dbt"], check=True)

@asset
def run_yolo_enrichment(run_dbt_transformations):
    subprocess.run(["python", "src/yolo_detect_images.py"], check=True)
