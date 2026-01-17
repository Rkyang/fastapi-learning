from pydantic import BaseModel, Field

class BookInfo(BaseModel):
    bookName: str = Field(..., min_length=2, max_length=20)
    author: str = Field(default='', min_length=2, max_length=10)
    publisher: str = Field(default='xx出版社')
    price: float = Field(..., gt=0)