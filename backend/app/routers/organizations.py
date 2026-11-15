from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Organization, OrganizationMembership, User
from app.audit import record_audit
from app.schemas import (
    OrganizationCreate,
    OrganizationList,
    OrganizationRead,
    OrganizationMemberList,
    OrganizationMemberRead,
    OrganizationMemberRoleUpdate,
)

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])

MANAGEABLE_ROLES = {"admin", "manager", "member"}


def require_org_manager(
    organization_id: str,
    current_user: User,
    db: Session,
) -> OrganizationMembership:
    membership = db.scalar(
        select(OrganizationMembership).where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == current_user.id,
            OrganizationMembership.is_active.is_(True),
        )
    )
    if membership is None:
        # Use 404 to avoid disclosing whether another tenant exists.
        raise HTTPException(status_code=404, detail="Organization not found")
    if membership.role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Organization administrator role required")
    return membership


@router.get("", response_model=OrganizationList)
def list_my_organizations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = db.execute(
        select(Organization, OrganizationMembership.role)
        .join(OrganizationMembership, OrganizationMembership.organization_id == Organization.id)
        .where(
            OrganizationMembership.user_id == current_user.id,
            OrganizationMembership.is_active.is_(True),
        )
        .order_by(Organization.name)
    ).all()
    return OrganizationList(items=[
        OrganizationRead(
            id=org.id, name=org.name, slug=org.slug, role=role, created_at=org.created_at
        ) for org, role in rows
    ])


@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
def create_organization(
    payload: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    slug = payload.slug.lower()
    if db.scalar(select(Organization).where(Organization.slug == slug)):
        raise HTTPException(status_code=409, detail="This organization identifier is already in use")
    organization = Organization(name=payload.name.strip(), slug=slug)
    db.add(organization)
    db.flush()
    db.add(OrganizationMembership(
        organization_id=organization.id, user_id=current_user.id, role="owner", is_active=True
    ))
    db.commit()
    db.refresh(organization)
    return OrganizationRead(
        id=organization.id,
        name=organization.name,
        slug=organization.slug,
        role="owner",
        created_at=organization.created_at,
    )


@router.get("/{organization_id}/members", response_model=OrganizationMemberList)
def list_organization_members(
    organization_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_org_manager(organization_id, current_user, db)
    rows = db.execute(
        select(OrganizationMembership, User)
        .join(User, User.id == OrganizationMembership.user_id)
        .where(OrganizationMembership.organization_id == organization_id)
        .order_by(User.full_name, User.email)
    ).all()
    return OrganizationMemberList(items=[
        OrganizationMemberRead(
            user_id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=membership.role,
            is_active=membership.is_active,
            joined_at=membership.created_at,
        )
        for membership, user in rows
    ])


@router.patch(
    "/{organization_id}/members/{member_user_id}/role",
    response_model=OrganizationMemberRead,
)
def update_organization_member_role(
    organization_id: str,
    member_user_id: str,
    payload: OrganizationMemberRoleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    actor_membership = require_org_manager(organization_id, current_user, db)
    target = db.scalar(
        select(OrganizationMembership).where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == member_user_id,
            OrganizationMembership.is_active.is_(True),
        )
    )
    if target is None:
        raise HTTPException(status_code=404, detail="Organization member not found")

    # Ownership transfer is intentionally excluded from this endpoint.
    # Only the owner can grant or revoke the administrator role.
    if target.role == "owner":
        raise HTTPException(status_code=403, detail="The owner role cannot be changed here")
    if payload.role == "owner":
        raise HTTPException(status_code=400, detail="Ownership transfer is not supported yet")
    if payload.role not in MANAGEABLE_ROLES:
        raise HTTPException(status_code=400, detail="Unsupported organization role")
    if actor_membership.role != "owner":
        if target.role == "admin" or payload.role == "admin":
            raise HTTPException(status_code=403, detail="Only the owner can manage administrators")

    previous_role = target.role
    target.role = payload.role
    record_audit(db, organization_id, current_user.id, "member.role_updated", "membership", target.id, {"user_id": member_user_id, "before": previous_role, "after": payload.role})
    db.commit()
    db.refresh(target)
    user = db.get(User, target.user_id)
    return OrganizationMemberRead(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=target.role,
        is_active=target.is_active,
        joined_at=target.created_at,
    )
