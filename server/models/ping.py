from pydantic import BaseModel


class Pong(BaseModel):
    status: bool

    class ConfigDict:
        json_schema_extra = {"example": {"status": True}}
