from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pydantic import EmailStr


class Settings(BaseSettings):
    app_title: str
    app_description: str
    path: str
    db_url: str
    secret: str = 'SECRET'
    model_config = SettingsConfigDict(env_file='.env')
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None


settings = Settings()
