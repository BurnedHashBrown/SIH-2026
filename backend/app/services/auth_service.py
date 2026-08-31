from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import verify_password, get_password_hash
from app.utils.constants import UserRole


class AuthService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = AuthService.get_user_by_email(db, email)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        existing_email = AuthService.get_user_by_email(db, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "EMAIL_EXISTS", "message": "A user with this email already exists."},
            )
            
        existing_emp = db.query(User).filter(User.employee_id == user_data.employee_id).first()
        if existing_emp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "EMPLOYEE_ID_EXISTS", "message": "A user with this Employee ID already exists."},
            )

        hashed_pw = get_password_hash(user_data.password)
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            employee_id=user_data.employee_id,
            password_hash=hashed_pw,
            role=user_data.role,
            department=user_data.department,
            is_active=user_data.is_active,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 50) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
        user = AuthService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "USER_NOT_FOUND", "message": "User not found."},
            )

        if user_update.name is not None:
            user.name = user_update.name
        if user_update.role is not None:
            user.role = user_update.role
        if user_update.department is not None:
            user.department = user_update.department
        if user_update.is_active is not None:
            user.is_active = user_update.is_active
        if user_update.password is not None:
            user.password_hash = get_password_hash(user_update.password)

        db.commit()
        db.refresh(user)
        return user


auth_service = AuthService()
