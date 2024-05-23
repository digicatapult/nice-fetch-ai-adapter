import os

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    VERITABLE_URL: str = os.getenv("VERITABLE_URL", "http://localhost:3010")
    PEER_URL: str = os.getenv("PEER_URL", "http://localhost:3001/api")
    AGENT_ADDRESS: str = os.getenv(
        "AGENT_ADDRESS",
        "agent1qt8q20p0vsp7y5dkuehwkpmsppvynxv8esg255fwz6el68rftvt5klpyeuj",
    )


settings = AppSettings()
