# -*- coding:utf-8 -*-
import os
from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "dev"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8081
    APP_VERSION: str = "0.0.1"
    BLOB_CONNECTION_STRING: str = ""


class DevelopmentConfig(Config):
    BLOB_CONNECTION_STRING = ""


class ProductionConfig(Config):
    BLOB_CONNECTION_STRING = ""


def get_config():
    env = os.getenv("ENV", "dev")
    config_type = {
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
