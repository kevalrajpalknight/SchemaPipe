from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Database settings
    database_host: str = "localhost"
    database_port: int = 5432
    database_user: str = "user"
    database_password: str = "password"
    database_name: str = "schemapipe_db"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.database_user}:{self.database_password}\
            @{self.database_host}:{self.database_port}/{self.database_name}"

    # Security settings
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS settings
    cors_origins: str | List[str] = []

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.cors_origins, str):
            return [
                origin.strip()
                for origin in self.cors_origins.split(",")
                if origin.strip()
            ]
        return self.cors_origins

    # Logging settings
    log_level: str = "INFO"
    log_format: str = "json"  # Options: "json", "plain"

    # Environment
    environment: str = "development"  # Options: "development", "production"

    # OpenAI Settings
    openai_api_key: str = "your_openai_api_key"

    class Config:
        env_file = ".env"
        extra = "allow"
        env_file_encoding = "utf-8"


settings = Settings()
