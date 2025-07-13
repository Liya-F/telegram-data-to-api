SELECT
  id,
  channel,
  text,
  date AS message_date,
  has_media,
  LENGTH(text) AS message_length
FROM raw.telegram_messages
