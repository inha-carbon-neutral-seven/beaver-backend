from pydantic import BaseModel


class Pong(BaseModel):
    message: bool

    class ConfigDict:
        json_schema_extra = {"example": {"message": True}}
