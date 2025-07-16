select *
from {{ ref('fct_messages') }}
where has_media = true and media_type is null
