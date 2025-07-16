-- models/marts/dim_channels.sql

select distinct
    channel_name as channel_id
from "telegram_data"."raw"."stg_telegram_messages"