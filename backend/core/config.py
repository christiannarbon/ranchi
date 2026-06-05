from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    cron_secret: str = "super_secret_cron_key"
    slack_bot_token: str
    slack_signing_secret: str
    google_places_api_key: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
