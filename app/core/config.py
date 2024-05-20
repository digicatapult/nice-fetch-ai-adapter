import os

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    VERITABLE_URL: str = os.getenv("VERITABLE_URL", "http://localhost:3010")
    PEER_URL: str = os.getenv("PEER_URL", "http://localhost:3001/api")


settings = AppSettings()