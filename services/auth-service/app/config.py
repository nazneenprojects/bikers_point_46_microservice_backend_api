from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database settings
    COSMOS_DB_URL: str
    COSMOS_KEY: str
    COSMOS_DB_NAME: str = "bikerpoint-auth-db"
    COSMOS_USER_CONTAINER: str = "users"

    # JWT settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App settings
    APP_NAME: str = "Bikers Point 46 Auth Service"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Try to load settings, provide helpful error message if .env is missing
try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    print("Make sure you have a .env file in the root directory with required variables:")
    print("- COSMOS_DB_URL")
    print("- COSMOS_KEY")
    print("- JWT_SECRET_KEY")
    raise