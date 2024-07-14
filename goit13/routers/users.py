from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, User, Token
from dependencies.database import get_db
from dependencies.authentication import create_access_token, create_refresh_token, get_current_user
from services.user_service import register_user, authenticate_user, send_verification_email
from fastapi.security import OAuth2PasswordRequestForm
from repositories.user_repository import verify_user
from fastapi import File, UploadFile
from services.user_service import upload_avatar



router = APIRouter()

@router.post("/users/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = register_user(db, user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    verification_token = create_access_token(data={"sub": db_user.email})
    send_verification_email(db_user.email, verification_token)
    return db_user

@router.post("/users/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.get("/users/verify")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = verify_user(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token or user not found")
    return {"message": "Email verified successfully"}

@router.post("/users/avatar", response_model=User)
def upload_user_avatar(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    avatar_url = upload_avatar(file)
    current_user.avatar_url = avatar_url
    db.commit()
    db.refresh(current_user)
    return current_user
