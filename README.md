# Telegram Data Pipeline

A data pipeline for scraping public Telegram channel messages, storing raw JSON data, and transforming it into a clean, analytics-ready PostgreSQL warehouse using dbt.

---

## Project Overview

This project automates the process of:

1. **Scraping** messages from public Telegram channels using [Telethon](https://github.com/LonamiWebs/Telethon).
2. **Storing** raw messages as JSON in a structured data lake (`data/raw/...`).
3. **Loading** the raw data into a PostgreSQL database.
4. **Transforming** the data using [dbt](https://www.getdbt.com/) into structured, analytical tables (star schema).
5. **Testing & Documenting** your data to ensure quality and trust.

---
## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/Liya-F/telegram-data-to-api.git
cd telegram-data-to-api
```
### 2.  Create .env file

```bash 
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
```
### 3. setup Python environment

```bash
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```
