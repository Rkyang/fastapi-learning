from fastapi import FastAPI
from routes import test_news

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(test_news.router, prefix="/api/news", tags=["news"])
