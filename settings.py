import os
import yaml
from typing import Optional
from pydantic_settings import BaseSettings


def load_yaml_settings(yaml_path: str) -> dict:
    if not os.path.exists(yaml_path):
        return {}
    with open(yaml_path, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)

    return yaml_data.get("services", {}).get("fastapi", {}).get("environment", {})


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

yaml_settings = load_yaml_settings("docker-compose.yml")
for key, value in yaml_settings.items():
    if not getattr(settings, key):
        setattr(settings, key, value)
