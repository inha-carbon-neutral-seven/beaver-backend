from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    llm_server_URL: str
    llm_server_ChatCompletion: str
    model_config = SettingsConfigDict(env_file="/app/server/.env")
