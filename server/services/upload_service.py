import os

STORAGE_PATH = "./server/storage/user1"  # 저장 경로, 세션 별 관리를 위해 폴더 분리해둠


async def upload_service(contents: bytes, filename: str, description: str) -> dict:
    # 기존 디렉토리 및 하위 내용 삭제 및 디렉토리 재생성
    if os.path.exists(STORAGE_PATH):
        for root, dirs, files in os.walk(STORAGE_PATH, topdown=False):
            for file_name in files:
                os.remove(os.path.join(root, file_name))
            for dir_name in dirs:
                os.rmdir(os.path.join(root, dir_name))
        os.rmdir(STORAGE_PATH)

    # raw_path에 저장
    raw_path = STORAGE_PATH + "/raw"
    os.makedirs(raw_path)
    with open(os.path.join(raw_path, filename), "wb") as fp:
        fp.write(contents)

    return {"filename": filename, "description": description}
