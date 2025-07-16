from .database import get_connection
from typing import List
from .schemas import Message, TopProduct, ChannelActivity

def get_top_products(limit: int) -> List[TopProduct]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT LOWER(word) as product, COUNT(*) as count
        FROM (
            SELECT unnest(string_to_array(message_text, ' ')) AS word
            FROM raw.stg_telegram_messages
            WHERE message_text IS NOT NULL
        ) AS words
        GROUP BY word
        ORDER BY count DESC
        LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return [TopProduct(product=row[0], count=row[1]) for row in rows]

def get_channel_activity(channel: str) -> List[ChannelActivity]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT date_id::TEXT, COUNT(*) as count
        FROM raw.fct_messages
        WHERE channel_id = %s
        GROUP BY date_id
        ORDER BY date_id
    """, (channel,))
    rows = cur.fetchall()
    conn.close()
    return [ChannelActivity(date=row[0], count=row[1]) for row in rows]

def search_messages(keyword: str) -> List[Message]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT message_id, channel_id, message_text, message_date
        FROM raw.fct_messages
        WHERE message_text ILIKE %s
        LIMIT 50
    """, (f"%{keyword}%",))
    rows = cur.fetchall()
    conn.close()
    return [Message(
        message_id=row[0],
        channel_id=row[1],
        message_text=row[2],
        message_date=row[3].isoformat()
    ) for row in rows]
