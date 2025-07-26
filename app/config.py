from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    access_token_expire_minutes: int
    algorithm: str
    base_url: str
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings() # type: ignore