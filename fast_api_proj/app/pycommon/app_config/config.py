import yaml
from pydantic_settings import BaseSettings
from threading import Lock
import os


conf_dir = "app/pycommon/app_config/config.yaml"
class Config(BaseSettings):
    DB_TYPE: str
    MAX_ADMIN_USERS: int


class ConfigSingleton:
    _instance = None
    _lock: Lock = Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._load_config()
            return cls._instance

    @staticmethod
    def _load_config():
        with open(conf_dir, "r") as f:
            config_data = yaml.safe_load(f)
        return Config(**config_data)



# Usage: Get the singleton instance
config = ConfigSingleton.get_instance()
