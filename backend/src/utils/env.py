from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    gpt_key: str

    model_config = SettingsConfigDict(env_file=".env")


env_settings = EnvSettings()
