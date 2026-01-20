from fastapi import FastAPI
from routes import news_category

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(news_category.router, prefix="/api/news", tags=["news"])
