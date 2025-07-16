
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select image_file
from "telegram_data"."raw"."fct_image_detections"
where image_file is null



  
  
      
    ) dbt_internal_test