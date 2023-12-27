from .storage import clear_storage, save_file, save_description

STORAGE_PATH = "./server/storage/user1"  # 저장 경로, 세션 별 관리를 위해 폴더 분리해둠


async def upload_file(contents: bytes, filename: str, description: str) -> dict:
    """
    클라이언트로부터 전달받은 파일을 웹 서버에 저장합니다
    """

    await clear_storage()
    await save_file(contents, filename)
    await save_description(description)

    return {"filename": filename, "description": description}
