-- models/staging/stg_telegram_messages.sql

with source as (
    select * from raw.raw_telegram_messages
),

renamed as (
    select
        message_id,
        channel_name,
        message_text,
        message_date,
        views,
        forwards,
        has_media,
        media_type,
        reply_count,
        reactions_json
    from source
)

select * from renamed
