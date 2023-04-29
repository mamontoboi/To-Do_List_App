"""The module contains the class Settings.
This class is used to access environmental variables for a Python application.
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """A pydantic model for accessing environmental variables."""

    DB_URL: str
    DB_NAME: str

    class Config:
        env_file = '.env'


settings = Settings()
