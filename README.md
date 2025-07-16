
# Telegram Medical Data Pipeline to Analytical API

An end-to-end data platform that extracts raw data from Ethiopian medical Telegram channels, transforms it into a clean analytical warehouse, enriches it with object detection, and exposes it via a FastAPI-powered API — all orchestrated with Dagster.

## Project Overview

This project simulates a real-world data engineering challenge:

> Scrape data from Telegram → Store it → Transform it → Enrich it → Serve it

You will use:
- `Telethon` for scraping messages and media
- `PostgreSQL` as your data warehouse
- `dbt` for transformation into a **star schema**
- `YOLOv8` for image-based object detection
- `FastAPI` to expose the data as an analytical API
- `Dagster` to orchestrate and automate the whole pipeline

## Tech Stack

| Layer          | Tool          | Purpose                                  |
|----------------|---------------|------------------------------------------|
| Data Source    | Telegram      | Medical product channels                 |
| Scraping       | Telethon      | Message + media scraping                 |
| Storage        | JSON, Images  | Data Lake (raw layer)                    |
| Data Warehouse | PostgreSQL    | Central structured storage               |
| Transformation | dbt           | Clean, model, and document data          |
| Enrichment     | YOLOv8        | Object detection on images               |
| API            | FastAPI       | Serve insights through HTTP endpoints    |
| Orchestration  | Dagster       | Schedule and observe the pipeline        |

## Project Structure

```
telegram-data-to-api/
│
├── data/
│   └── raw/
│       ├── telegram_messages/YYYY-MM-DD/channel.json
│       └── images/YYYY-MM-DD/channel_name/image_001.jpg
│
├── src/
│   ├── telegram_scraper.py
│   ├── download_images.py
│   ├── load_to_postgres.py
│   ├── yolo_detect_images.py
│
├── telegram_dbt/
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_telegram_messages.sql
│   │   └── marts/
│   │       ├── fct_messages.sql
│   │       ├── dim_channels.sql
│   │       └── dim_dates.sql
│
├── pipeline_project/
│   ├── pyproject.toml
│   └── pipeline_project/
│       ├── assets.py
│       ├── definitions.py
│
├── api/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
│
├── .env
├── requirements.txt
└── README.md
```

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Liya-F/telegram-data-to-api.git
cd telegram-data-to-api
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file:

```dotenv
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
PHONE=your_telegram_phone_number
POSTGRES_DB=telegram_data
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## How to Run Each Component

### Scrape Telegram Messages

```bash
python src/telegram_scraper.py
```

### Download Telegram Images

```bash
python src/download_images.py
```

### Load JSON to PostgreSQL

```bash
python src/load_to_postgres.py
```

### Run YOLOv8 Object Detection

```bash
python src/yolo_detect_images.py
```

### Run dbt Transformations

```bash
cd telegram_dbt
dbt run
```

### Launch the API Server

```bash
cd api
uvicorn main:app --reload
```

Access at: http://localhost:8000/docs

## API Endpoints

- `GET /api/reports/top-products?limit=10`
- `GET /api/channels/{channel}/activity`
- `GET /api/search/messages?keyword=paracetamol`

## Orchestrate with Dagster

### 1. Launch Dagster UI

```bash
cd pipeline_project
dagster dev
```

Visit: http://localhost:3000

### 2. Run the Full Pipeline in Dagster UI

Click:
- `scrape_telegram_data`
- `→ load_raw_to_postgres`
- `→ run_dbt_transformations`
- `→ run_yolo_enrichment`

