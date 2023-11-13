from pydantic import BaseModel


class Question(BaseModel):
    """
    질의 request를 받는 양식을 작성합니다.
    """

    message: str

    class ConfigDict:
        json_schema_extra = {"example": {"message": "한국의 수도는 어디야?"}}
