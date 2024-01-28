"""
POST /upload 
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""
from io import StringIO
from pandas import read_csv

from .storage import clear_storage, save_file, load_df_path


def upload_file(contents: bytes, filename: str, description: str) -> dict:
    """
    클라이언트로부터 전달받은 파일을 웹 서버에 저장합니다
    """

    # 저장소를 초기화하고 파일을 저장합니다.
    clear_storage()
    save_file(contents, filename, description)

    # 테이블 데이터면 documentation을 추가로 생성합니다.
    df_path = load_df_path()
    if df_path:
        save_table_documentation(table_name=description, df_path=df_path)

    return {"filename": filename, "description": description}


def save_table_documentation(table_name: str, df_path: str):
    """
    테이블을 설명하는 documentation을 만들어 텍스트 문서로 저장합니다.
    """
    df = read_csv(df_path)

    string_buffer = StringIO()
    df.info(buf=string_buffer)
    df_info = string_buffer.getvalue()

    documentation = f"""
# table documentation
- This document is a description of the table file attached by the retailer to request analysis of his/her data.
- NOTE: The original table name is '{table_name}', but a new name that matches the table information is needed. 

## information of dataframe
- result of pd.DataFrame.info() is below:
```
{df_info}
```

## Brief table contents
- First 5 rows of the DataFrame is below:
```
{str(df.head())}
```
"""
    contents = documentation.encode(encoding="utf-8")
    description = f"{table_name}-documentation"
    save_file(contents=contents, filename="docs.txt", description=description)
