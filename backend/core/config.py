from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    cron_secret: str
    slack_bot_token: str
    slack_signing_secret: str
    google_places_api_key: str

    # Comma-separated list of allowed CORS origins (the frontend URLs).
    cors_origins: str = "http://localhost:5173"
    # Optional/opt-in regex for matching origins (e.g. Vercel preview deploys).
    cors_origin_regex: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
