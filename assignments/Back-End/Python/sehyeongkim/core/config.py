import os

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    ENV: str = 'dev'
    DEBUG: bool = True

    DB_URL: str

    class Config:
        case_sensitive = False


class DevConfig(BaseConfig):
    ENV: str = 'dev'

    class Config:
        env_file = 'dev.env'


class ProdConfig(BaseConfig):
    ENV: str = 'prod'

    class Config:
        env_file = 'prod.env'


def get_config():
    env = os.getenv('ENV', 'dev')
    config_type = {
        'dev': DevConfig,
        'prod': ProdConfig,
    }
    return config_type[env]()

config = get_config()
