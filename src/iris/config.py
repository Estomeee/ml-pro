from typing import Literal

from pydantic_settings import BaseSettings 


class Settings(BaseSettings):
    model_path: str = "artifacts/model.joblib"
    database_url: str | None = None
    log_level: Literal["INFO"] = "INFO"

    model_config = {
        "env_file": ".env",
        "protected_namespaces": (),
    }

settings = Settings()