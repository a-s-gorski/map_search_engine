import os

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings, PostgresDsn

env_file = find_dotenv()

if env_file:
    load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "my_project"
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_URL")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DBNAME")

    SQLALCHEMY_DATABASE_URI: PostgresDsn = PostgresDsn.build(
        scheme="postgresql",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_SERVER,
        port=POSTGRES_PORT,
        path=f"/{POSTGRES_DB}"
    )

    class Config:
        env_file = ".env"


settings = Settings()
