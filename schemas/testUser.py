from pydantic import BaseModel

class TestUserSchemaBase(BaseModel):

    user_name: str
    password: str