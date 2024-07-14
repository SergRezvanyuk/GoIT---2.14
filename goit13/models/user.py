from sqlalchemy import Column, Integer, String, Boolean
from dependencies.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    """
    User model for the database.

    :param id: Primary key
    :param email: User email
    :param hashed_password: User password (hashed)
    :param is_verified: Verification status
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    contacts = relationship("Contact", back_populates="owner")