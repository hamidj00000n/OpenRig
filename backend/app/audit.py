import json
from app.models import AuditLog

def record_audit(db, organization_id, actor_user_id, action, target_type, target_id, details=None):
    db.add(AuditLog(organization_id=organization_id, actor_user_id=actor_user_id,
        action=action, target_type=target_type, target_id=target_id,
        details=json.dumps(details or {}, separators=(",", ":"), sort_keys=True)))
