from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseModel):
    api_key: str
    model: str
    reasoning_effort: str


class RedisSettings(BaseModel):
    host: str
    port: int = 6379
    db: int = 0
    password: str | None = None

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}" + (f"?password={self.password}" if self.password else "")


class Settings(BaseSettings):
    app_name: str = "not-only-poke-bot"
    env: str = "development"
    debug: bool = True

    openai: OpenAISettings = Field(..., alias="openai")
    redis: RedisSettings = Field(..., alias="redis")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        populate_by_name=True,
        env_nested_delimiter="_",
        env_nested_max_split=1
    )


settings = Settings()
