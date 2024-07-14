from sqlalchemy.orm import Session
from models.contact import Contact
from schemas.contact import ContactCreate, ContactUpdate
from datetime import date, timedelta

def get_contact(db: Session, contact_id: int):
    """
    Retrieve a contact by ID.

    :param db: Database session
    :param contact_id: Contact ID
    :return: Contact object or None
    """
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """
    Retrieve all contacts for a user.

    :param db: Database session
    :param user_id: User ID
    :param skip: Number of records to skip
    :param limit: Limit number of records
    :return: List of contacts
    """
    return db.query(Contact).filter(Contact.owner_id == user_id).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate, user_id: int):
    """
    Create a new contact.

    :param db: Database session
    :param contact: ContactCreate schema
    :param user_id: User ID
    :return: Contact object
    """
    db_contact = Contact(**contact.dict(), owner_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    """
    Update an existing contact.

    :param db: Database session
    :param contact_id: Contact ID
    :param contact: ContactUpdate schema
    :return: Updated contact object or None
    """
    db_contact = get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    """
    Delete a contact by ID.

    :param db: Database session
    :param contact_id: Contact ID
    :return: Deleted contact object or None
    """
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, user_id: int, query: str):
    """
    Search contacts by query.

    :param db: Database session
    :param user_id: User ID
    :param query: Search query
    :return: List of matching contacts
    """
    return db.query(Contact).filter(
        Contact.owner_id == user_id,
        (Contact.first_name.contains(query)) | 
        (Contact.last_name.contains(query)) | 
        (Contact.email.contains(query))
    ).all()

def get_upcoming_birthdays(db: Session, user_id: int, days: int = 30):
    """
    Retrieve contacts with upcoming birthdays.

    :param db: Database session
    :param user_id: User ID
    :param within_days: Days within which to search for birthdays
    :return: List of contacts with upcoming birthdays
    """
    today = date.today()
    upcoming_date = today + timedelta(days=days)
    return db.query(Contact).filter(
        Contact.owner_id == user_id,
        Contact.birthday >= today,
        Contact.birthday <= upcoming_date
    ).all()
