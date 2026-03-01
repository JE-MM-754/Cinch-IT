"""Application configuration — loaded from .env file."""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./cinchit.db"  # SQLite fallback for dev

    # Apollo
    apollo_api_key: str = ""

    # SendGrid
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = "outreach@getcinchmsp.com"
    sendgrid_from_name: str = "Cinch IT Boston"

    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    # OpenAI
    openai_api_key: str = ""

    # Google Places
    google_places_api_key: str = ""

    # App
    app_secret_key: str = "dev-secret-change-me"
    app_env: str = "development"
    app_port: int = 8000
    frontend_url: str = "http://localhost:3000"

    # Safety: test mode
    test_mode: bool = True
    test_contact_name: str = "Jamie Erickson"
    test_contact_email: str = "Erickson.JamesD@gmail.com"
    test_contact_phone: str = "+15084049628"

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
