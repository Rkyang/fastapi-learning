from fastapi import FastAPI

app = FastAPI()

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
