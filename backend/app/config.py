import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./openrig.db")
SECRET_KEY = os.getenv("OPENRIG_SECRET_KEY", "")
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "30"))
CORS_ORIGINS = [item.strip() for item in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if item.strip()]

if not SECRET_KEY and os.getenv("OPENRIG_ENV", "development") == "production":
    raise RuntimeError("OPENRIG_SECRET_KEY must be configured in production.")
if not SECRET_KEY:
    SECRET_KEY = "local-development-only-change-before-deployment"
