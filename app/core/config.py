# app/core/config.py

from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    # Base de datos
    DATABASE_URL: str

    # Seguridad
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # Aplicación
    APP_NAME: str = "Peluquería App"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia global de configuración
# Se importa desde cualquier parte del proyecto con:
# from app.core.config import settings
settings = Settings()