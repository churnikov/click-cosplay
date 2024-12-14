from pydantic import Field, SecretStr
from loguru import logger

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    opper_api_key: str = Field(alias='OPPER_API_KEY')
    openai_api_key: str = Field(alias='OPENAI_API_KEY')

    anthropic_api_key: str = Field(alias='ANTHROPIC_API_KEY')
    footway_api_key: str = Field(alias='FOOTWAY-API-KEY')
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()