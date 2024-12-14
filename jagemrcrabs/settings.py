from pydantic import Field, SecretStr
from loguru import logger

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    opper_api_key: SecretStr = Field(alias='OPPER_API_KEY')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()