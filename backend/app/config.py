from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url: str = "sqlite:///./novacart_dev.db"
    jwt_secret_key: str = "dev-only-change-me"
    jwt_expire_minutes: int = 1440
    frontend_url: str = "http://localhost:3000"
    admin_email: str = "admin@novacart.local"
    admin_password: str = "ChangeThisAdminPassword123!"
    seed_demo_products: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
