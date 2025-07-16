from dagster import Definitions
from .assets import (
    scrape_telegram_data,
    load_raw_to_postgres,
    run_dbt_transformations,
    run_yolo_enrichment,
)

# Group all pipeline steps (assets)
all_assets = [
    scrape_telegram_data,
    load_raw_to_postgres,
    run_dbt_transformations,
    run_yolo_enrichment,
]

# Export them to Dagster
defs = Definitions(assets=all_assets)
