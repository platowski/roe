from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    workos_client_id: str
    workos_api_key: str

    model_config = SettingsConfigDict(env_file=".env")


env_settings = EnvSettings()
