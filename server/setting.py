from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    llm_server_URL: str = "EMPTY_URL"
    model_config = SettingsConfigDict(env_file="/app/server/.env")
