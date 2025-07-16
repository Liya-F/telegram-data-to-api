from fastapi import FastAPI
from .crud import get_top_products, get_channel_activity, search_messages
from .schemas import TopProduct, ChannelActivity, Message

app = FastAPI(title="Telegram Medical Data API")

@app.get("/")
def root():
    return {"message": "API is working!"}

@app.get("/api/reports/top-products", response_model=list[TopProduct])
def top_products(limit: int = 10):
    return get_top_products(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=list[ChannelActivity])
def channel_activity(channel_name: str):
    return get_channel_activity(channel_name)

@app.get("/api/search/messages", response_model=list[Message])
def search(keyword: str):
    return search_messages(keyword)
