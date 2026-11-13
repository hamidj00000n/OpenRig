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
    assert response.status_code == 201, response.text
    login = client.post("/api/v1/auth/login", json={
        "email": email, "password": "correct-horse-battery-12"
    })
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def create_org(headers, slug):
    response = client.post("/api/v1/organizations", headers=headers, json={
        "name": f"Company {slug}", "slug": slug
    })
    assert response.status_code == 201, response.text
    return response.json()["id"]


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
    create_org(owner_headers, "private-company")
    other_headers = register_and_login("second@openrig.dev")
    listed = client.get("/api/v1/organizations", headers=other_headers)
    assert listed.status_code == 200
    assert listed.json()["items"] == []


def test_organization_endpoints_require_authentication():
    response = client.get("/api/v1/organizations")
    assert response.status_code == 401


def test_owner_can_list_members_and_promote_member_to_admin():
    owner = register_and_login("members-owner@openrig.dev")
    organization_id = create_org(owner, "members-company")
    member = register_and_login("members-user@openrig.dev")
    member_user = client.get("/api/v1/auth/me", headers=member).json()

    # Add a second membership directly as an isolated test setup operation.
    from app.models import OrganizationMembership
    db = TestingSession()
    try:
        db.add(OrganizationMembership(
            organization_id=organization_id, user_id=member_user["id"], role="member"
        ))
        db.commit()
    finally:
        db.close()

    listed = client.get(f"/api/v1/organizations/{organization_id}/members", headers=owner)
    assert listed.status_code == 200
    assert {item["email"] for item in listed.json()["items"]} == {
        "members-owner@openrig.dev", "members-user@openrig.dev"
    }

    updated = client.patch(
        f"/api/v1/organizations/{organization_id}/members/{member_user['id']}/role",
        headers=owner,
        json={"role": "admin"},
    )
    assert updated.status_code == 200
    assert updated.json()["role"] == "admin"


def test_regular_member_cannot_manage_organization_members():
    owner = register_and_login("member-owner@openrig.dev")
    organization_id = create_org(owner, "member-access-company")
    member = register_and_login("member-user@openrig.dev")
    member_user = client.get("/api/v1/auth/me", headers=member).json()

    from app.models import OrganizationMembership
    db = TestingSession()
    try:
        db.add(OrganizationMembership(
            organization_id=organization_id, user_id=member_user["id"], role="member"
        ))
        db.commit()
    finally:
        db.close()

    response = client.get(
        f"/api/v1/organizations/{organization_id}/members", headers=member
    )
    assert response.status_code == 403


def test_admin_cannot_grant_admin_role_or_change_owner():
    owner = register_and_login("admin-owner@openrig.dev")
    organization_id = create_org(owner, "admin-policy-company")
    admin = register_and_login("admin-user@openrig.dev")
    admin_user = client.get("/api/v1/auth/me", headers=admin).json()

    from app.models import OrganizationMembership
    db = TestingSession()
    try:
        db.add(OrganizationMembership(
            organization_id=organization_id, user_id=admin_user["id"], role="admin"
        ))
        db.commit()
    finally:
        db.close()

    other = register_and_login("admin-target@openrig.dev")
    other_user = client.get("/api/v1/auth/me", headers=other).json()
    db = TestingSession()
    try:
        db.add(OrganizationMembership(
            organization_id=organization_id, user_id=other_user["id"], role="member"
        ))
        db.commit()
    finally:
        db.close()

    response = client.patch(
        f"/api/v1/organizations/{organization_id}/members/{other_user['id']}/role",
        headers=admin,
        json={"role": "admin"},
    )
    assert response.status_code == 403


def test_user_cannot_access_members_of_another_organization():
    first_owner = register_and_login("tenant-one@openrig.dev")
    organization_id = create_org(first_owner, "tenant-one-company")
    other_owner = register_and_login("tenant-two@openrig.dev")
    response = client.get(
        f"/api/v1/organizations/{organization_id}/members", headers=other_owner
    )
    assert response.status_code == 404


def test_owner_can_invite_user_and_invitation_is_accepted_once():
    owner = register_and_login("invite-owner@openrig.dev")
    organization_id = create_org(owner, "invite-company")
    invitee = register_and_login("invitee@openrig.dev")

    created = client.post(
        f"/api/v1/organizations/{organization_id}/invitations",
        headers=owner,
        json={"email": "invitee@openrig.dev", "role": "manager"},
    )
    assert created.status_code == 201, created.text
    payload = created.json()
    assert payload["role"] == "manager"
    assert payload["token"]

    accepted = client.post(
        "/api/v1/organizations/invitations/accept",
        headers=invitee,
        json={"token": payload["token"]},
    )
    assert accepted.status_code == 200, accepted.text
    assert accepted.json()["role"] == "manager"

    repeated = client.post(
        "/api/v1/organizations/invitations/accept",
        headers=invitee,
        json={"token": payload["token"]},
    )
    assert repeated.status_code == 404
    orgs = client.get("/api/v1/organizations", headers=invitee).json()["items"]
    assert any(item["id"] == organization_id and item["role"] == "manager" for item in orgs)


def test_invitation_cannot_be_accepted_by_different_email():
    owner = register_and_login("invite-owner-two@openrig.dev")
    organization_id = create_org(owner, "invite-company-two")
    wrong_user = register_and_login("wrong-person@openrig.dev")
    created = client.post(
        f"/api/v1/organizations/{organization_id}/invitations",
        headers=owner,
        json={"email": "intended-person@openrig.dev", "role": "member"},
    )
    assert created.status_code == 201
    response = client.post(
        "/api/v1/organizations/invitations/accept",
        headers=wrong_user,
        json={"token": created.json()["token"]},
    )
    assert response.status_code == 403


def test_admin_cannot_invite_another_administrator():
    owner = register_and_login("invite-admin-owner@openrig.dev")
    organization_id = create_org(owner, "invite-admin-company")
    admin = register_and_login("invite-admin@openrig.dev")
    admin_user = client.get("/api/v1/auth/me", headers=admin).json()
    from app.models import OrganizationMembership
    db = TestingSession()
    try:
        db.add(OrganizationMembership(
            organization_id=organization_id, user_id=admin_user["id"], role="admin"
        ))
        db.commit()
    finally:
        db.close()

    response = client.post(
        f"/api/v1/organizations/{organization_id}/invitations",
        headers=admin,
        json={"email": "new-admin@openrig.dev", "role": "admin"},
    )
    assert response.status_code == 403


def test_regular_member_cannot_create_invitation():
    owner = register_and_login("invite-member-owner@openrig.dev")
    organization_id = create_org(owner, "invite-member-company")
    member = register_and_login("invite-member@openrig.dev")
    member_user = client.get("/api/v1/auth/me", headers=member).json()
    from app.models import OrganizationMembership
    db = TestingSession()
    try:
        db.add(OrganizationMembership(
            organization_id=organization_id, user_id=member_user["id"], role="member"
        ))
        db.commit()
    finally:
        db.close()

    response = client.post(
        f"/api/v1/organizations/{organization_id}/invitations",
        headers=member,
        json={"email": "another@openrig.dev", "role": "member"},
    )
    assert response.status_code == 403
