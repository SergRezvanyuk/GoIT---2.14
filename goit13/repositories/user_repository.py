from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate

def get_user(db: Session, user_id: int):
    """
    Retrieve a user by ID.

    :param db: Database session
    :param user_id: User ID
    :return: User object or None
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by email.

    :param db: Database session
    :param email: User email
    :return: User object or None
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    """
    Create a new user.

    :param db: Database session
    :param user: UserCreate schema
    :return: User object
    """
    db_user = User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_user(db: Session, token: str):
    """
    Verify a user by token.

    :param db: Database session
    :param token: Verification token
    :return: User object or None
    """
    user = db.query(User).filter(User.verification_token == token).first()
    if user:
        user.is_verified = True
        db.commit()
        db.refresh(user)
    return user