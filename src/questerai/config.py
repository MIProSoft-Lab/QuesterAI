from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "QuesterAI"
    debug: bool = True
    database_url: str = "postgresql+asyncpg://questerai:questerai@localhost:5432/questerai_db"
    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
