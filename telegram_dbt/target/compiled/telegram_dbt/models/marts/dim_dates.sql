-- models/marts/dim_dates.sql

select distinct
    cast(date_trunc('day', message_date) as date) as date_id
from "telegram_data"."raw"."stg_telegram_messages"