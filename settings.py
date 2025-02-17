from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file(local: bool = False) -> Path:
    return Path(__file__).parent / ".env.local" if local else Path(__file__).parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=get_env_file(), env_file_encoding='utf-8')
    telegram_api_key: str
    mongo_client: str
    mongo_db_name: str
    mongo_collection_name: str
    WEBHOOK_HOST: str
    WEBHOOK_PATH: str
    main_domain: str

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}"


# Инициализация настроек
settings = Settings()
