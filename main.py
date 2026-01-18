from contextlib import asynccontextmanager

from fastapi import FastAPI, Path, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config.db_config import DATABASE_URL
from models.TestUser import TestUser
from schemas.bookInfo import BookInfo
from schemas.newsInfo import NewsInfo
from schemas.testUser import TestUserNew

# ORM 建表
# 创建异步引擎
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True, #可选，输出sql日志
    pool_size=10, # 活跃连接数
    max_overflow=20 # 额外连接数
)
# 建表
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(TestUser.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan start")
    await create_tables()
    yield
    print('lifespan end')

app = FastAPI(lifespan=lifespan)

# 路由匹配中使用orm
# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    # 绑定数据库引擎
    bind=async_engine,
    # 指定会话类
    class_=AsyncSession,
    # 会话不过期，不重查库
    expire_on_commit=False
)
# 依赖项，获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
# 查库
@app.get('/user/getUser')
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestUser))
    # 查所有
    # users = result.scalars().all()
    # 第一条
    users = result.scalars().first()
    return users
@app.get('/user/getUser/{id}')
async def get_users_id(id: int, db: AsyncSession = Depends(get_db)):
    # result = await db.get(TestUser, id)
    # return result

    result = await db.execute(select(TestUser).where(TestUser.id == id))
    return result.scalar_one_or_none()
@app.get('/user/search')
async def get_users_search(db: AsyncSession = Depends(get_db)):
    # like
    # result = await db.execute(select(TestUser).where(TestUser.user_name.like('%三%')))
    # 与或非
    # result = await db.execute(select(TestUser).where((TestUser.user_name.like('%三%')) & (TestUser.password == '123456')))
    # in
    id_list = [1,3]
    result = await db.execute(select(TestUser).where(TestUser.id.in_(id_list)))
    users = result.scalars().all()
    return users
# 插库
@app.post('/user/new')
async def get_users_search(user_new: TestUserNew, db: AsyncSession = Depends(get_db)):
    obj = TestUser(**user_new.__dict__)
    query_result = await db.execute(select(func.max(TestUser.id)))
    max_id: int = query_result.scalar()
    obj.id = (max_id + 1)
    db.add(obj)
    await db.commit()
    return user_new

# 依赖注入 Depends
async def common_params(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=20, le=100)
):
    return {"skip": skip, "limit": limit}

@app.get("/new/list")
async def news_list(common = Depends(common_params)):
    return common

# 中间件
@app.middleware("http")
async def middleware2(request, call_next):
    print('mw2 start')
    response = await call_next(request)
    print('mw2 end')
    return response

@app.middleware("http")
async def middleware1(request, call_next):
    print('mw1 start')
    response = await call_next(request)
    print('mw1 end')
    return response

# 异常响应处理
@app.get("/news/{id}")
async def get_news(id: int):
    id_list = [1,2,3,4,5,6]
    if id not in id_list:
        raise HTTPException(status_code=404, detail='not exist')
    return {"id": id}

# 自定义响应类型
@app.get("/news/diy_resp/{id}", response_model=NewsInfo)
async def get_news(id: int):
    return {
        "id": id,
        "title": f'this is {id} book',
        "content": "it's great book"
    }

# 响应类型-响应对象方式
@app.get("/file")
async def get_file():
    path = './files/1.jpg'
    return FileResponse(path)

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
