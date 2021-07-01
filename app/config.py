from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "fastapi mongodb"
    DEBUG: bool = False
    MONGO_DETAILS: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
