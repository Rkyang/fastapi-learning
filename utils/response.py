from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def success_response(message: str = "success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    # 任何fastapi、pydantic、orm对象都正常响应
    return JSONResponse(content=jsonable_encoder(content))