from fastapi import APIRouter

from ..services.process import run
from ..services.debug import run_process as process_debug

from ..models.process import ProcessInput, ProcessOutput

process_router = APIRouter()


@process_router.post("/process")
async def process(process_input: ProcessInput) -> ProcessOutput:
    """
    업로드한 파일을 적절한 데이터 형태로 처리합니다.

    1. "recap" 선택           : 파일 임베딩 및 recap 생성
    2. "recommendation" 선택  : recommendation 생성
    3. "chart" 선택           : chart 생성

    input: json
    ```
    {
        "type" : "recap"
    }
    ```
    """
    process_type = process_input.type
    return run(process_type=process_type)


# DEBUG


@process_router.post("/process_debug")
async def debug(process_input: ProcessInput) -> ProcessOutput:
    """
    [테스트] 업로드한 파일을 적절한 데이터 형태로 처리합니다.

    1. "recap" 선택           : 파일 임베딩 및 recap 생성
    2. "recommendation" 선택  : recommendation 생성
    3. "chart" 선택           : chart 생성

    input: json
    ```
    {
        "type" : "recap"
    }
    ```
    """
    process_type = process_input.type
    return await process_debug(process_type=process_type)
