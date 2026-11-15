from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import AuditLog, OrganizationMembership, OrganizationPermission, User
from app.schemas import AuditLogList, AuditLogRead, PermissionList, PermissionRead, PermissionUpdate
from app.audit import record_audit

router=APIRouter(prefix="/api/v1/organizations",tags=["permissions and audit"])
MODULES=("rigs","equipment","warehouse","maintenance","procurement","reports")
ROLES=("admin","manager","member")

def get_membership(org_id,user,db):
    row=db.scalar(select(OrganizationMembership).where(OrganizationMembership.organization_id==org_id,OrganizationMembership.user_id==user.id,OrganizationMembership.is_active.is_(True)))
    if row is None: raise HTTPException(status_code=404,detail="Organization not found")
    return row

@router.get("/{organization_id}/permissions",response_model=PermissionList)
def list_permissions(organization_id:str,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    member=get_membership(organization_id,current_user,db)
    if member.role not in {"owner","admin"}: raise HTTPException(status_code=403,detail="Organization administrator role required")
    rows=db.scalars(select(OrganizationPermission).where(OrganizationPermission.organization_id==organization_id)).all()
    saved={(r.role,r.module):r for r in rows}
    items=[]
    for role in ROLES:
        for module in MODULES:
            row=saved.get((role,module))
            defaults={"admin":(True,True,True,False),"manager":(True,True,True,False),"member":(True,False,False,False)}[role]
            items.append(PermissionRead(role=role,module=module,can_view=row.can_view if row else defaults[0],can_create=row.can_create if row else defaults[1],can_update=row.can_update if row else defaults[2],can_delete=row.can_delete if row else defaults[3]))
    return PermissionList(items=items)

@router.put("/{organization_id}/permissions",response_model=PermissionRead)
def update_permission(organization_id:str,payload:PermissionUpdate,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    member=get_membership(organization_id,current_user,db)
    if member.role!="owner": raise HTTPException(status_code=403,detail="Only the organization owner can configure permissions")
    if (payload.can_create or payload.can_update or payload.can_delete) and not payload.can_view: raise HTTPException(status_code=422,detail="Write permissions require view permission")
    row=db.scalar(select(OrganizationPermission).where(OrganizationPermission.organization_id==organization_id,OrganizationPermission.role==payload.role,OrganizationPermission.module==payload.module))
    if row is None:
        row=OrganizationPermission(organization_id=organization_id,role=payload.role,module=payload.module); db.add(row); db.flush()
    before={k:getattr(row,k) for k in ("can_view","can_create","can_update","can_delete")}
    for k in before: setattr(row,k,getattr(payload,k))
    record_audit(db,organization_id,current_user.id,"permission.updated","permission",row.id,{"role":payload.role,"module":payload.module,"before":before,"after":{k:getattr(row,k) for k in before}})
    db.commit(); db.refresh(row)
    return PermissionRead(role=row.role,module=row.module,can_view=row.can_view,can_create=row.can_create,can_update=row.can_update,can_delete=row.can_delete)

@router.get("/{organization_id}/audit-logs",response_model=AuditLogList)
def list_audit_logs(organization_id:str,limit:int=100,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    member=get_membership(organization_id,current_user,db)
    if member.role not in {"owner","admin"}: raise HTTPException(status_code=403,detail="Organization administrator role required")
    if limit<1 or limit>200: raise HTTPException(status_code=422,detail="Limit must be between 1 and 200")
    rows=db.scalars(select(AuditLog).where(AuditLog.organization_id==organization_id).order_by(AuditLog.created_at.desc()).limit(limit)).all()
    return AuditLogList(items=[AuditLogRead(id=r.id,actor_user_id=r.actor_user_id,action=r.action,target_type=r.target_type,target_id=r.target_id,details=r.details,created_at=r.created_at) for r in rows])
