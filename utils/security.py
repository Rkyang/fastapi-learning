from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# 加密
def get_password_hash(password: str):
    return pwd_context.hash(password)

# 验证
def validate_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)