from pydantic import BaseModel


class Question(BaseModel):
    message: str

    class ConfigDict:
        json_schema_extra = {"example": {"message": "한국의 수도는 어디야?"}}


class Answer(BaseModel):
    message: str

    class ConfigDict:
        json_schema_extra = {"example": {"message": "한국의 수도는 서울입니다."}}
