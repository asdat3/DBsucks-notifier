from pydantic_settings import BaseSettings
from typing import List, Dict, Any
import json


class Settings(BaseSettings):
    # Deutsche Bahn API credentials
    db_client_id: str
    db_client_secret: str
    
    # Discord webhook URL
    discord_webhook_url: str
    
    # Station configurations - JSON string from environment variable
    station_configs: str

    # UTC correction
    utc_correction: int

    # Hours to check
    hours_to_check: str
    
    @property
    def config_list(self) -> List[Dict[str, Any]]:
        """Parse the station_configs JSON string into a list of configuration dictionaries."""
        try:
            return json.loads(self.station_configs)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in station_configs: {e}")
        
    @property
    def hours_to_check_list(self) -> List[int]:
        """Parse the hours_to_check string into a list of integers."""
        return json.loads(self.hours_to_check)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a global settings instance
settings = Settings()
