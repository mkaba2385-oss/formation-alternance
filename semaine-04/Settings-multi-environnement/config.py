import os
from typing import Literal
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    ENV: Literal["dev", "staging", "prod"]
    DEBUG: bool = False
    DATABASE_URL: str
    JWT_SECRET: str
    API_KEY: str
    
    # Permet de lire depuis un fichier .env localement
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class DevSettings(AppSettings):
    ENV: Literal["dev"] = "dev"
    DEBUG: bool = True

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_local_db(cls, v: str) -> str:
        if ".com" in v or ".app" in v:
            raise ValueError("En environnement 'dev', la base de données ne doit pas pointer vers un domaine distant (.com ou .app).")
        return v


class StagingSettings(AppSettings):
    ENV: Literal["staging"] = "staging"

    @field_validator("API_KEY")
    @classmethod
    def validate_staging_api_key(cls, v: str) -> str:
        if v.startswith("prod_"):
            raise ValueError("En environnement 'staging', la clé d'API ne doit pas être celle de production (préfixe 'prod_').")
        return v


class ProductionSettings(AppSettings):
    ENV: Literal["prod"] = "prod"
    DEBUG: bool = False

    @model_validator(mode="after")
    def validate_prod_security(self) -> "ProductionSettings":
        if self.DEBUG is True:
            raise ValueError("Erreur critique : DEBUG doit impérativement être 'False' en production.")
        
        if len(self.JWT_SECRET) < 64:
            raise ValueError("Erreur critique : En production, JWT_SECRET doit contenir au moins 64 caractères pour des raisons de sécurité.")
            
        return self


def get_settings() -> AppSettings:
    """
    Instancie la bonne classe de configuration en fonction de la variable d'environnement 'ENV'.
    Déclenche automatiquement les validations Pydantic au démarrage.
    """
    env = os.getenv("ENV", "dev").lower()
    
    if env == "prod":
        return ProductionSettings()
    elif env == "staging":
        return StagingSettings()
    else:
        return DevSettings()