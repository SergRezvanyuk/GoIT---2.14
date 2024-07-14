from sqlalchemy.orm import Session
from repositories.user_repository import create_user, get_user_by_email
from schemas.user import UserCreate
from passlib.context import CryptContext
import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import UploadFile


cloudinary.config(
  cloud_name = "your_cloud_name",
  api_key = "your_api_key",
  api_secret = "your_api_secret"
)


def upload_avatar(file: UploadFile):
    result = cloudinary.uploader.upload(file.file)
    return result['secure_url']


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def register_user(db: Session, user: UserCreate):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return None
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    return create_user(db, user)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def send_verification_email(email: str, token: str):
    message = f"Please verify your email by clicking on the following link: http://localhost:8000/api/v1/users/verify?token={token}"
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(message)
    msg['Subject'] = 'Verify your email'
    msg['From'] = 'no-reply@example.com'
    msg['To'] = email

    with smtplib.SMTP('localhost') as server:
        server.send_message(msg)