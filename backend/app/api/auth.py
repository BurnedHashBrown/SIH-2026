from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, UserBasicResponse
from app.schemas.user import UserResponse
from app.models.user import User
from app.services.auth_service import auth_service
from app.services.audit_service import audit_service
from app.utils.security import create_access_token
from app.utils.constants import AuditAction
from app.api.deps import get_current_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse, summary="User login")
def login(login_data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """Authenticate user with email and password, returning JWT bearer token."""
    user = auth_service.authenticate_user(db, email=login_data.email, password=login_data.password)
    client_ip = request.client.host if request.client else None

    if not user:
        audit_service.log_event(
            db=db,
            action=AuditAction.LOGIN,
            ip_address=client_ip,
            metadata={"email": login_data.email, "success": False, "reason": "Invalid credentials"},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Incorrect email or password."},
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=user.id,
        extra_claims={"role": user.role.value, "email": user.email},
    )

    audit_service.log_event(
        db=db,
        action=AuditAction.LOGIN,
        user_id=user.id,
        entity_type="User",
        entity_id=str(user.id),
        ip_address=client_ip,
        metadata={"email": user.email, "role": user.role.value, "success": True},
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserBasicResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse, summary="Get current logged-in user profile")
def get_me(current_user: User = Depends(get_current_user)):
    """Return profile data of authenticated user."""
    return current_user


@router.post("/logout", summary="User logout")
def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log out current user and record audit trail."""
    client_ip = request.client.host if request.client else None
    audit_service.log_event(
        db=db,
        action=AuditAction.LOGOUT,
        user_id=current_user.id,
        entity_type="User",
        entity_id=str(current_user.id),
        ip_address=client_ip,
    )
    return {"message": "Successfully logged out."}
