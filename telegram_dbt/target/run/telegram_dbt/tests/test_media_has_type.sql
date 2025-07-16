
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- tests/test_media_has_type.sql

select *
from "telegram_data"."raw"."fct_messages"
where has_media = true and media_type is null
  
  
      
    ) dbt_internal_test