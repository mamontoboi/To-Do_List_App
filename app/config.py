from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    DB_NAME: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    class Config:
        env_file = '.env'


settings = Settings()
