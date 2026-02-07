from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import User
from repositories.user_repo import UserRepo
from schemas.user_schemas import UserSchema
from schemas.Token_schemas import Token, TokenRefresh, LoginRequest
from utils.jwt_handler import create_tokens, verify_token

router = APIRouter()


@router.post("/signup")
def signup(user: UserSchema, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    # Convert Pydantic schema to SQLAlchemy model
    existing_user = user_repo.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = User(email=user.email, password=user.password)
    user_repo.add_user(db_user)
    return {"message": "User signed up successfully"}


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return access and refresh tokens."""
    user_repo = UserRepo(db)
    user = user_repo.get_user_by_email(credentials.email)
    
    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return create_tokens(user.id, user.email)


@router.post("/refresh", response_model=Token)
def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Get new access and refresh tokens using a valid refresh token."""
    payload = verify_token(token_data.refresh_token, token_type="refresh")
    
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_repo = UserRepo(db)
    user = user_repo.get_user_by_email(payload.get("email"))
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return create_tokens(user.id, user.email)