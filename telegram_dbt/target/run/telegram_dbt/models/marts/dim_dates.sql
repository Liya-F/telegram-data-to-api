
  create view "telegram_data"."raw"."dim_dates__dbt_tmp"
    
    
  as (
    -- models/marts/dim_dates.sql

select distinct
    cast(date_trunc('day', message_date) as date) as date_id
from "telegram_data"."raw"."stg_telegram_messages"
  );