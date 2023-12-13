from pydantic import BaseModel


# 서버 상태를 확인할 때 사용하는 모델
class Pong(BaseModel):
    status: bool

    class ConfigDict:
        json_schema_extra = {"example": {"status": True}}
