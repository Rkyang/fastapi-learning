from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse

from models.bookInfo import BookInfo

app = FastAPI()

# 响应类型-装饰器方式
@app.get("/html", response_class=HTMLResponse)
async def html():
    return '<h1>这是一级标题</h1>'

# 请求体参数
@app.post("/book/new")
async def new_book(book_info: BookInfo):
    return {"book_info": book_info}

# 查询参数 Query类型
@app.get("/book/query")
async def book_query(
        category: str = Query('python开发', min_length=5, max_length=255),
        price: float = Query(0, gt=50, lt=100),
):
    return {"category": category, "price": price}

# 路径参数 Path类型
@app.get("/news/byName/{news_name}")
async def news_by_name(news_name: str = Path(..., min_length=2, max_length=10, description='按分类名称获取，名称长度2-10')):
    return {"news_name": news_name}

@app.get("/news/byId/{news_id}")
async def news_by_id(news_id: int = Path(..., gt=0, lt=101, description='按分类id获取，id范围1-100')):
    return {"新闻分类id": news_id}

# 路径参数
@app.get("/user/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id, "user_name": f"用户id={user_id}"}

@app.get("/book/{id}")
async def get_book(id: int):
    return {"id": id, "title": f"这是第 {id} 本书"}

# init
@app.get("/user/hello")
async def user_hello():
    return {"msg": "我正在学习FastAPI……"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
