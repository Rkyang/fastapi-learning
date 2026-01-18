from pydantic import BaseModel

class TestUserNew(BaseModel):

    user_name: str
    password: str