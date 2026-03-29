from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "yourdb"
    DB_USER: str = "youruser"
    DB_PASSWORD: str = "yourpass"

    # Comma-separated list — edit in .env to add/remove origins
    CORS_ORIGINS: str = (
        "http://localhost:3000,"
        "http://localhost:5173,"
        "http://localhost:5174,"
        "http://localhost:5175"
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
