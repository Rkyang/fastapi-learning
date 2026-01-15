from pydantic import BaseModel

class BookInfo(BaseModel):
    bookName: str
    author: str
    publisher: str
    price: float