from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.models.user import User
from app.services.auth_service import auth_service
from app.services.audit_service import audit_service
from app.utils.constants import UserRole, AuditAction
from app.api.deps import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserResponse], summary="List all users")
def list_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    """Admin endpoint to list registered system users."""
    return auth_service.list_users(db, skip=skip, limit=limit)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create a new user")
def create_user(
    user_in: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    """Admin endpoint to create a new user."""
    new_user = auth_service.create_user(db, user_in)
    client_ip = request.client.host if request.client else None
    audit_service.log_event(
        db=db,
        action=AuditAction.USER_CREATE,
        user_id=current_user.id,
        entity_type="User",
        entity_id=str(new_user.id),
        ip_address=client_ip,
        metadata={"new_user_email": new_user.email, "role": new_user.role.value},
    )
    return new_user


@router.get("/{user_id}", response_model=UserResponse, summary="Get user by ID")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve user details by ID."""
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "You do not have access to this user profile."},
        )
    user = auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "User not found."},
        )
    return user
