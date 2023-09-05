from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str
    secret_jwt_key: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
