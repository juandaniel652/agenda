from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    FRONTEND_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # ignora variables de más en entorno
    )

settings = Settings()