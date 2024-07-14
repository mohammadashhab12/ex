from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_TYPE: str = 'redis'
    MAX_ADMIN_USERS: int = 5

    class Config:
        env_file = ".env"



config = Config()
