import re

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Organization, OrganizationMembership, User
from app.schemas import OrganizationCreate, OrganizationList, OrganizationRead

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


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
    slug = re.sub(r"[^a-z0-9-]", "", payload.slug.lower())
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
