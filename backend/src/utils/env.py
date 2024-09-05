from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    cpu_count: int = 1
    model_config = SettingsConfigDict(env_file=".env")


env_settings = EnvSettings()
