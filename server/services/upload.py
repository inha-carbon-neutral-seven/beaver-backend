from .storage import clear_storage, save_file, save_description

async def upload_file(contents: bytes, filename: str, description: str) -> dict:
    """
    클라이언트로부터 전달받은 파일을 웹 서버에 저장합니다
    """

    await clear_storage()
    await save_file(contents, filename, description)
    # await save_description(description)

    return {"filename": filename, "description": description}
