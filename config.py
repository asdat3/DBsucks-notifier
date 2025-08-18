from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Deutsche Bahn API credentials
    db_client_id: str
    db_client_secret: str
    
    # Discord webhook URL
    discord_webhook_url: str
    
    # Station configuration
    station_name: str = "Berlin Hbf"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a global settings instance
settings = Settings()
