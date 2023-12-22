import os

STORAGE_PATH = "./server/storage/user1"  # 저장 경로, 세션 별 관리를 위해 폴더 분리해둠


async def clear_storage() -> None:
    raw_path = STORAGE_PATH + "/raw"
    embed_path = STORAGE_PATH + "/embed"
    structured_path = STORAGE_PATH + "/structured"

    # 기존 디렉토리 및 하위 내용 삭제
    if os.path.exists(STORAGE_PATH):
        for root, dirs, files in os.walk(STORAGE_PATH, topdown=False):
            for file_name in files:
                os.remove(os.path.join(root, file_name))
            for dir_name in dirs:
                os.rmdir(os.path.join(root, dir_name))
        os.rmdir(STORAGE_PATH)

    #  디렉토리 재생성
    os.makedirs(raw_path)
    os.makedirs(embed_path)
    os.makedirs(structured_path)


async def save_raw_file(contents: bytes, filename: str) -> None:
    # file_path = os.path.join(STORAGE_PATH + "/raw", filename)
    file_path = os.path.join(STORAGE_PATH + "/structured", filename)

    with open(file_path, "wb") as fp:
        fp.write(contents)


async def save_description(description: str) -> None:
    description_path = os.path.join(STORAGE_PATH + "/raw", "description.txt")

    # 문자열을 UTF-8로 인코딩하여 bytes로 변환
    encoded_description = description.encode("utf-8")

    with open(description_path, "wb") as fp:
        fp.write(encoded_description)


async def load_csv_file() -> str:
    """
    path에 있는 첫 번째 csv 파일 경로를 전달하는 함수
    """
    structured_data_path = "./server/storage/user1/structured/"

    csv_files = [file for file in os.listdir(structured_data_path) if file.endswith(".csv")]

    if not csv_files:
        raise FileNotFoundError("디렉토리에 CSV 파일을 찾을 수 없습니다.")

    csv_file = os.path.join(structured_data_path, csv_files[0])

    return csv_file
