from sqlalchemy.orm import Session
from models.contact import Contact
from schemas.contact import ContactCreate, ContactUpdate
from datetime import date, timedelta

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Contact).filter(Contact.owner_id == user_id).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate, user_id: int):
    db_contact = Contact(**contact.dict(), owner_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, user_id: int, query: str):
    return db.query(Contact).filter(
        Contact.owner_id == user_id,
        (Contact.first_name.contains(query)) | 
        (Contact.last_name.contains(query)) | 
        (Contact.email.contains(query))
    ).all()

def get_upcoming_birthdays(db: Session, user_id: int):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(
        Contact.owner_id == user_id,
        Contact.birthday >= today,
        Contact.birthday <= next_week
    ).all()
