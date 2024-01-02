from fastapi import Request

user_map = {"sequence": 1000}


def get_user_id() -> int:
    """
    get user_id
    """
    return user_map["user_id"]


def set_user_id(request: Request):
    """
    set user_id
    """
    host = request.headers.get("host")
    origin = request.headers.get("origin")
    key = f"host:{host}::origin:{origin}"

    if key not in user_map:
        # sequence를 가져와 업데이트합니다
        user_map["sequence"] = user_map["sequence"] + 1

        # 가져온 sequence를 이용해 새 user를 등록합니다
        user_map[key] = user_map["sequence"]

    user_map["user_id"] = user_map[key]
