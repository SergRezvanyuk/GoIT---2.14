from sqlalchemy.orm import Session
from repositories.contact_repository import (
    create_contact, get_contacts, get_contact, update_contact, delete_contact,
    search_contacts, get_upcoming_birthdays
)
from schemas.contact import ContactCreate, ContactUpdate

def create_new_contact(db: Session, contact: ContactCreate, user_id: int):
    return create_contact(db, contact, user_id)

def get_all_contacts(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return get_contacts(db, user_id, skip, limit)

def get_contact_by_id(db: Session, contact_id: int):
    return get_contact(db, contact_id)

def update_existing_contact(db: Session, contact_id: int, contact: ContactUpdate):
    return update_contact(db, contact_id, contact)

def delete_contact_by_id(db: Session, contact_id: int):
    return delete_contact(db, contact_id)

def search_user_contacts(db: Session, user_id: int, query: str):
    return search_contacts(db, user_id, query)

def get_contacts_with_upcoming_birthdays(db: Session, user_id: int):
    return get_upcoming_birthdays(db, user_id)
