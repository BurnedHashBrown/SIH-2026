from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.rule import RuleResponse, RuleCreate
from app.models.rule import Rule
from app.models.user import User
from app.api.deps import get_current_user, require_role
from app.utils.constants import UserRole

router = APIRouter(prefix="/rules", tags=["Rules"])


@router.get("", response_model=List[RuleResponse], summary="List all Legal Metrology compliance rules")
def list_rules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all active versioned compliance rules."""
    return db.query(Rule).order_by(Rule.rule_code.asc()).all()


@router.get("/{rule_id}", response_model=RuleResponse, summary="Get rule by ID")
def get_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve rule definition details."""
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "RULE_NOT_FOUND", "message": "Rule not found."},
        )
    return rule


@router.post("", response_model=RuleResponse, status_code=status.HTTP_201_CREATED, summary="Create rule (Admin only)")
def create_rule(
    rule_in: RuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    """Admin endpoint to register a new Legal Metrology regulatory rule."""
    existing = db.query(Rule).filter(Rule.rule_code == rule_in.rule_code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "RULE_EXISTS", "message": f"Rule with code '{rule_in.rule_code}' already exists."},
        )
    rule = Rule(**rule_in.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule
