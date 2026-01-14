from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/news/byName/{news_name}")
async def news_by_name(news_name: str = Path(..., min_length=2, max_length=10, description='按分类名称获取，名称长度2-10')):
    return {"news_name": news_name}

@app.get("/news/byId/{news_id}")
async def news_by_id(news_id: int = Path(..., gt=0, lt=101, description='按分类id获取，id范围1-100')):
    return {"新闻分类id": news_id}

@app.get("/user/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id, "user_name": f"用户id={user_id}"}

@app.get("/book/{id}")
async def get_book(id: int):
    return {"id": id, "title": f"这是第 {id} 本书"}

@app.get("/user/hello")
async def user_hello():
    return {"msg": "我正在学习FastAPI……"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
