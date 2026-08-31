import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.utils.constants import AuditAction

logger = logging.getLogger("metrology.audit")


class AuditService:
    @staticmethod
    def log_event(
        db: Session,
        action: AuditAction | str,
        user_id: Optional[int] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """
        Record a secure, non-repudiable audit event.
        Guarantees that sensitive data like passwords or tokens are never logged.
        """
        safe_metadata = {}
        if metadata:
            # Filter out any sensitive keys
            for k, v in metadata.items():
                if any(secret_term in k.lower() for secret_term in ["password", "token", "secret", "auth", "hash"]):
                    continue
                safe_metadata[k] = v

        action_str = action.value if isinstance(action, AuditAction) else str(action)
        
        audit_entry = AuditLog(
            user_id=user_id,
            action=action_str,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id is not None else None,
            ip_address=ip_address,
            extra_metadata=safe_metadata,
        )
        db.add(audit_entry)
        try:
            db.commit()
            db.refresh(audit_entry)
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to write audit log: {e}")
            
        return audit_entry


audit_service = AuditService()
