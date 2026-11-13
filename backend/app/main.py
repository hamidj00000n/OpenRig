from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.database import Base, engine
from app import models  # noqa: F401
from app.routers import auth, organizations, invitations

app = FastAPI(
    title="OpenRig API",
    description="OpenRig authentication, organization, and invitation services",
    version="0.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router)
app.include_router(organizations.router)
app.include_router(invitations.router)


@app.on_event("startup")
def initialize_local_database():
    # Development bootstrap only. Production deployments must use versioned migrations.
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "openrig-api"}
