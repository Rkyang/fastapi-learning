from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel


class TestUser(BaseModel):
    __tablename__ = "test_user"
    __table_args__ = {
        'comment': '这是测试用户表，使用orm创建'
    }

    id: Mapped[int] = mapped_column(primary_key=True, comment='用户id')
    user_name: Mapped[str] = mapped_column(String(255), nullable=False, comment='用户名')
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment='密码')