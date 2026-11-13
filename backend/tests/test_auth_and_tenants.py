import os

os.environ["OPENRIG_SECRET_KEY"] = "test-only-secret-key-not-for-production"
os.environ["DATABASE_URL"] = "sqlite://"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


def override_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_db
client = TestClient(app)


def register_and_login(email: str):
    response = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Test User", "password": "correct-horse-battery-12"
    })
    assert response.status_code == 201
    login = client.post("/api/v1/auth/login", json={
        "email": email, "password": "correct-horse-battery-12"
    })
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_user_can_create_and_list_own_organization():
    headers = register_and_login("owner@openrig.dev")
    created = client.post("/api/v1/organizations", headers=headers, json={
        "name": "North Drilling", "slug": "north-drilling"
    })
    assert created.status_code == 201
    assert created.json()["role"] == "owner"
    listed = client.get("/api/v1/organizations", headers=headers)
    assert [item["slug"] for item in listed.json()["items"]] == ["north-drilling"]


def test_organizations_are_not_visible_to_other_users():
    owner_headers = register_and_login("first@openrig.dev")
    client.post("/api/v1/organizations", headers=owner_headers, json={
        "name": "Private Company", "slug": "private-company"
    })
    other_headers = register_and_login("second@openrig.dev")
    listed = client.get("/api/v1/organizations", headers=other_headers)
    assert listed.status_code == 200
    assert listed.json()["items"] == []


def test_organization_endpoints_require_authentication():
    response = client.get("/api/v1/organizations")
    assert response.status_code == 401
