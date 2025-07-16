-- tests/test_media_has_type.sql

select *
from "telegram_data"."raw"."fct_messages"
where has_media = true and media_type is null