from pydantic import BaseModel

class NewsInfo(BaseModel):
    id: int
    title: str
    content: str