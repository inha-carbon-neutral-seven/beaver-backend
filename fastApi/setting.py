from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    llm_server_URL: str

    model_config = SettingsConfigDict(env_file="/app/fastApi/.env")


