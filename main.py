from fastapi import FastAPI
from routes import news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    # 允许源
    allow_origins=["*"],
    # 允许携带token
    allow_credentials=True,
    # 允许请求方法类型
    allow_methods=["*"],
    # 允许请求头
    allow_headers=["*"]
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(news.router, prefix="/api/news", tags=["news"])
