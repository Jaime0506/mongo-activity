# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    APP_NAME: str = "LibraryAPI"
    APP_ENV: str = "dev"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000

    # Mongo - forma A (URI directa) o B (partes)
    MONGODB_URI: str | None = None
    MONGODB_DB: str = "librarydb"
    MONGODB_COLLECTION_CARS: str = "cars"

    # Partes (usadas solo si no hay MONGODB_URI)
    MONGODB_USER: str | None = None
    MONGODB_PASSWORD: str | None = None
    MONGODB_HOST: str = "prueba.gqpx3rt.mongodb.net"
    MONGODB_PARAMS: str = "retryWrites=true&w=majority"

    @computed_field  # pydantic v2
    @property
    def mongo_uri(self) -> str:
        """
        URI final a usar por Motor.
        Prioriza MONGODB_URI. Si no existe, intenta construirla con las partes.
        """
        if self.MONGODB_URI:
            return self.MONGODB_URI

settings = Settings()
