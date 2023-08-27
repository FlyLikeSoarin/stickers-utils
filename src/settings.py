import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    telegram_bot_token: str
    telegram_bot_name: str
    telegram_user_id: int
    telegram_addsticker_prefix: str

    model_config = pydantic_settings.SettingsConfigDict(env_file=(".env",))


settings = Settings()
