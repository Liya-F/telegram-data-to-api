select distinct
    cast(date_trunc('day', message_date) as date) as date_id
from {{ ref('stg_telegram_messages') }}
