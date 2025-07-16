
    
    

select
    message_id as unique_field,
    count(*) as n_records

from "telegram_data"."raw"."stg_telegram_messages"
where message_id is not null
group by message_id
having count(*) > 1


