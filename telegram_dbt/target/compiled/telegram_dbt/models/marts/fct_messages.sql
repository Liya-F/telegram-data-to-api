-- models/marts/fct_messages.sql

select
    message_id,
    channel_name as channel_id,
    cast(date_trunc('day', message_date) as date) as date_id,
    message_text,
    length(message_text) as message_length,
    has_media,
    media_type,
    views,
    forwards,
    reply_count
from "telegram_data"."raw"."stg_telegram_messages"