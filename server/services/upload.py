"""
POST /upload 
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

from .storage import clear_storage, save_file


def upload_file(contents: bytes, filename: str, description: str) -> dict:
    """
    클라이언트로부터 전달받은 파일을 웹 서버에 저장합니다
    """

    clear_storage()
    save_file(contents, filename, description)

    return {"filename": filename, "description": description}
