import os
from datetime import timedelta

# =====================================================
# SECURITY
# =====================================================

# IMPORTANT:
# In production, NEVER hardcode this.
# Always inject via environment variables or secrets manager.

# ✅ This supports:

# Environment-based secrets

# Token expiration control

# Future extensibility (issuer, audience)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_ME_SUPER_SECRET_KEY")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# =====================================================
# JWT SETTINGS (OPTIONAL EXTENSIONS)
# =====================================================
JWT_ISSUER = os.getenv("JWT_ISSUER", "ecommerce-platform")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "ecommerce-clients")


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 15

    # App
    app_name: str = "auth-service"
    environment: str = "dev"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
