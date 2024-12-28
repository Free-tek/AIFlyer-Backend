import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


path = Path.cwd()

env_path = path / ".env"
load_dotenv(dotenv_path=env_path, override=True)

ENVIRONMENT = os.environ.get("ENVIRONMENT", "DEVELOPMENT")


if ENVIRONMENT == "PRODUCTION":
    """
    set prod environment variables

    """
    google_config_base64 = os.environ.get("GOOGLE_CONFIG_BASE64", None)
    api_key: str = os.environ.get("API_KEY", None)
    storage_bucket: str = os.environ.get("STORAGE_BUCKET", None)
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", None)
    anthropic_api_key: str = os.environ.get("ANTHROPIC_API_KEY", None)
    smtp_server: str = os.environ.get("SMTP_SERVER", None)
    smtp_port: str = os.environ.get("SMTP_PORT", None)
    smtp_username: str = os.environ.get("SMTP_USERNAME", None)
    smtp_password: str = os.environ.get("SMTP_PASSWORD", None)
    sender_email: str = os.environ.get("SENDER_EMAIL", None)
    freepik_api_key: str = os.environ.get("FREEPIK_API_KEY", None)
    pass

elif ENVIRONMENT == "DEVELOPMENT" or ENVIRONMENT == "LOCAL":
    """
    set dev environment variables

    """
    google_config_base64 = os.environ.get("GOOGLE_CONFIG_BASE64", None)
    api_key: str = os.environ.get("API_KEY", None)
    storage_bucket: str = os.environ.get("STORAGE_BUCKET", None)
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", None)
    anthropic_api_key: str = os.environ.get("ANTHROPIC_API_KEY", None)
    smtp_server: str = os.environ.get("SMTP_SERVER", None)
    smtp_port: str = os.environ.get("SMTP_PORT", None)
    smtp_username: str = os.environ.get("SMTP_USERNAME", None)
    smtp_password: str = os.environ.get("SMTP_PASSWORD", None)
    sender_email: str = os.environ.get("SENDER_EMAIL", None)
    freepik_api_key: str = os.environ.get("FREEPIK_API_KEY", None)
else:
    pass



class Settings(BaseSettings):
    """
    Set config variables on settins class

    """

    API_V1_0STR: str = "/v1"
    API_TITLE: str = os.environ.get("API_TITLE", "STRUCTUREME SEARCH SERVICE APIS")
    API_ROOT_PATH: str = os.environ.get("API_ROOT_PATH", "/api")    
    GOOGLE_CONFIG_BASE64: str = google_config_base64  
    API_KEY: str = api_key
    STORAGE_BUCKET: str = storage_bucket
    OPENAI_API_KEY: str = openai_api_key
    ANTHROPIC_API_KEY: str = anthropic_api_key
    SMTP_SERVER: str = smtp_server
    SMTP_PORT: str = smtp_port
    SMTP_USERNAME: str = smtp_username
    SMTP_PASSWORD: str = smtp_password
    SENDER_EMAIL: str = sender_email
    FREEPIK_API_KEY: str = freepik_api_key

settings = Settings()