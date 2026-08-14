from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    federal_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire: int = 30

    # O .env também atende ao Docker Compose; chaves alheias à aplicação são ignoradas.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="Utf-8",
        extra="ignore",
    )

settings = Settings()
