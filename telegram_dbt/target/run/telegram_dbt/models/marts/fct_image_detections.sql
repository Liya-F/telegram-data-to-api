
  create view "telegram_data"."raw"."fct_image_detections__dbt_tmp"
    
    
  as (
    select
    channel_name,
    image_file,
    detected_class,
    confidence_score
from raw.image_detections
  );