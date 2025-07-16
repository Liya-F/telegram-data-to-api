from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    message_id: int
    channel_id: str
    message_text: str
    message_date: str

class TopProduct(BaseModel):
    product: str
    count: int

class ChannelActivity(BaseModel):
    date: str
    count: int
