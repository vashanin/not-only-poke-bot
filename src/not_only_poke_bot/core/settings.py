from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseModel):
    api_key: str
    model: str
    reasoning_effort: str


class Settings(BaseSettings):
    app_name: str = "not-only-poke-bot"
    env: str = "development"
    debug: bool = True

    openai: OpenAISettings = Field(..., alias="openai")

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", populate_by_name=True, env_nested_delimiter="_", env_nested_max_split=1
    )


settings = Settings()
