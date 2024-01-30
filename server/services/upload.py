"""
POST /upload 
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""
from io import StringIO
from pandas import DataFrame
import numpy as np
from pydantic import BaseModel

from .storage import clear_storage, save_file, load_dataframe


class DatetimeRange(BaseModel):
    column_name: str
    min: str
    max: str


def upload_file(contents: bytes, filename: str, description: str) -> dict:
    """
    클라이언트로부터 전달받은 파일을 웹 서버에 저장합니다
    """

    # 저장소를 초기화하고 파일을 저장합니다.
    clear_storage()
    save_file(contents, filename, description)

    # 테이블 데이터면 documentation을 추가로 생성합니다.
    df = load_dataframe()
    if isinstance(df, DataFrame):
        save_table_documentation(table_name=description, df=df)

    return {"filename": filename, "description": description}


def save_table_documentation(table_name: str, df: DataFrame):
    """
    테이블을 설명하는 documentation을 만들어 텍스트 문서로 저장합니다.
    """
    df_info = get_df_info(df=df)
    datetime_ranges = get_datetime_ranges(df=df)

    documentation = f"""
## 테이블 내용 요약
- 이 테이블은 소매업자가 첨부한 데이터입니다. 
- 테이블의 첫 5행 내용을 확인하여 문서의 흐름을 이해할 수 있습니다:
{str(df.head())}


## 테이블 내용 유형
- 테이블 내용의 유형은 아래와 같습니다:
{str(df.dtypes)}


## 테이블 내용 정보
- pd.DataFrame.info()의 결과입니다.
- 아래를 살펴보며 필요한 키워드를 파싱할 수 있습니다:
{df_info}

"""

    for datetime_range in datetime_ranges:
        datetime_text = f"""
## datetime format column "{datetime_range.column_name}" 추가 설명
- {datetime_range.min} 부터 {datetime_range.max} 까지의 날짜 범위를 가집니다. 

"""
        documentation += datetime_text

    # documentation 저장
    contents = documentation.encode(encoding="utf-8")
    description = f"{table_name}-documentation"
    save_file(contents=contents, filename="docs.txt", description=description)


def get_df_info(df: DataFrame) -> str:
    string_buffer = StringIO()
    df.info(buf=string_buffer)
    df_info = string_buffer.getvalue()
    return df_info


def get_datetime_ranges(df: DataFrame) -> list:
    datetime_columns = df.select_dtypes(include=[np.datetime64])
    datetime_ranges = []

    # datetime_columns의 각 column들의 최소 date, 최대 date를 date_bandwidthes에 저장
    for column in datetime_columns.columns:
        datetime_range = DatetimeRange(
            column_name=column,
            min=str(df[column].min()),
            max=str(df[column].max()),
        )
        datetime_ranges.append(datetime_range)

    return datetime_ranges
