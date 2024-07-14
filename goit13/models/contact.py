from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from dependencies.database import Base
from sqlalchemy.orm import relationship
from models.user import User

class Contact(Base):
    """
    Contact model for the database.

    :param id: Primary key
    :param first_name: First name
    :param last_name: Last name
    :param email: Email address
    :param phone_number: Phone number
    :param birthday: Birthday
    :param additional_info: Additional information
    :param owner_id: Foreign key to the owner (User)
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    additional_info = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="contacts")


