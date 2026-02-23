from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Car Finder"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "prd"

    DATABASE_HOST: str = Field(...)
    DATABASE_NAME: str = Field(...)
    DATABASE_USER: str = Field(...)
    DATABASE_PASSWORD: str = Field(...)
    DATABASE_PORT: int = Field(default=5432)

    @computed_field
    @property
    def database_url(self) -> str:
        build_url = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.DATABASE_HOST,
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            port=self.DATABASE_PORT,
            path=self.DATABASE_NAME,
        )

        return str(build_url)


    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
    )


settings = Settings()
