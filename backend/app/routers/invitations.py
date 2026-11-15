import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.audit import record_audit
from app.dependencies import get_current_user
from app.models import Organization, OrganizationInvitation, OrganizationMembership, User
from app.schemas import InvitationAccept, InvitationCreate, InvitationCreated, InvitationList, InvitationRead

router = APIRouter(prefix="/api/v1/organizations", tags=["organization invitations"])
INVITATION_DAYS = 7


def require_invitation_manager(organization_id: str, user: User, db: Session) -> OrganizationMembership:
    membership = db.scalar(select(OrganizationMembership).where(
        OrganizationMembership.organization_id == organization_id,
        OrganizationMembership.user_id == user.id,
        OrganizationMembership.is_active.is_(True),
    ))
    if membership is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    if membership.role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Organization administrator role required")
    return membership


@router.post("/{organization_id}/invitations", response_model=InvitationCreated, status_code=201)
def create_invitation(
    organization_id: str,
    payload: InvitationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    actor = require_invitation_manager(organization_id, current_user, db)
    organization = db.get(Organization, organization_id)
    email = str(payload.email).lower()
    if actor.role != "owner" and payload.role == "admin":
        raise HTTPException(status_code=403, detail="Only the owner can invite administrators")
    existing_user = db.scalar(select(User).where(User.email == email))
    if existing_user:
        existing_membership = db.scalar(select(OrganizationMembership).where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == existing_user.id,
        ))
        if existing_membership:
            raise HTTPException(status_code=409, detail="User already has a membership in this organization")
    pending = db.scalar(select(OrganizationInvitation).where(
        OrganizationInvitation.organization_id == organization_id,
        OrganizationInvitation.email == email,
        OrganizationInvitation.status == "pending",
    ))
    if pending:
        raise HTTPException(status_code=409, detail="A pending invitation already exists for this email")
    raw_token = secrets.token_urlsafe(32)
    invitation = OrganizationInvitation(
        organization_id=organization_id,
        email=email,
        role=payload.role,
        token_hash=hashlib.sha256(raw_token.encode()).hexdigest(),
        status="pending",
        expires_at=datetime.now(timezone.utc) + timedelta(days=INVITATION_DAYS),
        created_by_user_id=current_user.id,
    )
    db.add(invitation)
    db.flush()
    record_audit(db, organization_id, current_user.id, "invitation.created", "invitation", invitation.id, {"email": email, "role": payload.role})
    db.commit()
    db.refresh(invitation)
    return InvitationCreated(
        id=invitation.id, email=invitation.email, role=invitation.role,
        status=invitation.status, expires_at=invitation.expires_at,
        created_at=invitation.created_at, token=raw_token,
    )


@router.get("/{organization_id}/invitations", response_model=InvitationList)
def list_invitations(
    organization_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_invitation_manager(organization_id, current_user, db)
    rows = db.scalars(select(OrganizationInvitation).where(
        OrganizationInvitation.organization_id == organization_id,
        OrganizationInvitation.status == "pending",
    ).order_by(OrganizationInvitation.created_at.desc())).all()
    return InvitationList(items=[InvitationRead(
        id=item.id, email=item.email, role=item.role, status=item.status,
        expires_at=item.expires_at, created_at=item.created_at,
    ) for item in rows])


@router.post("/invitations/accept", status_code=200)
def accept_invitation(
    payload: InvitationAccept,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    token_hash = hashlib.sha256(payload.token.encode()).hexdigest()
    invitation = db.scalar(select(OrganizationInvitation).where(
        OrganizationInvitation.token_hash == token_hash,
        OrganizationInvitation.status == "pending",
    ))
    if invitation is None:
        raise HTTPException(status_code=404, detail="Invitation is invalid or already used")
    now = datetime.now(timezone.utc)
    expires_at = invitation.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at <= now:
        invitation.status = "expired"
        db.commit()
        raise HTTPException(status_code=410, detail="Invitation has expired")
    if current_user.email.lower() != invitation.email.lower():
        raise HTTPException(status_code=403, detail="Sign in with the email address invited")
    membership = db.scalar(select(OrganizationMembership).where(
        OrganizationMembership.organization_id == invitation.organization_id,
        OrganizationMembership.user_id == current_user.id,
    ))
    if membership:
        if membership.is_active:
            raise HTTPException(status_code=409, detail="You are already a member of this organization")
        membership.is_active = True
        membership.role = invitation.role
    else:
        db.add(OrganizationMembership(
            organization_id=invitation.organization_id,
            user_id=current_user.id,
            role=invitation.role,
            is_active=True,
        ))
    invitation.status = "accepted"
    invitation.accepted_at = now
    record_audit(db, invitation.organization_id, current_user.id, "invitation.accepted", "invitation", invitation.id, {"email": invitation.email, "role": invitation.role})
    db.commit()
    organization = db.get(Organization, invitation.organization_id)
    return {"organization_id": organization.id, "organization_name": organization.name, "role": invitation.role}
