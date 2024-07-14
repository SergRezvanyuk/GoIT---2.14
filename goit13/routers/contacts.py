from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.contact import ContactCreate, ContactUpdate, Contact
from dependencies.database import get_db
from dependencies.authentication import get_current_user
from services.contact_service import (
    create_new_contact, get_all_contacts, get_contact_by_id, update_existing_contact, 
    delete_contact_by_id, search_user_contacts, get_contacts_with_upcoming_birthdays
)
from models.user import User
from fastapi_limiter.depends import RateLimiter


router = APIRouter()

@router.post("/contacts/", response_model=Contact, status_code=201, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def create_contact(
    contact: ContactCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return create_new_contact(db, contact, current_user.id)

@router.get("/contacts/", response_model=list[Contact])
def read_contacts(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return get_all_contacts(db, current_user.id, skip, limit)

@router.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_contact = get_contact_by_id(db, contact_id)
    if not db_contact or db_contact.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int, 
    contact: ContactUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_contact = get_contact_by_id(db, contact_id)
    if not db_contact or db_contact.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contact not found")
    return update_existing_contact(db, contact_id, contact)

@router.delete("/contacts/{contact_id}", response_model=Contact)
def delete_contact(
    contact_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_contact = get_contact_by_id(db, contact_id)
    if not db_contact or db_contact.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contact not found")
    return delete_contact_by_id(db, contact_id)

@router.get("/contacts/search", response_model=list[Contact])
def search_contacts(
    query: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return search_user_contacts(db, current_user.id, query)

@router.get("/contacts/birthdays", response_model=list[Contact])
def upcoming_birthdays(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return get_contacts_with_upcoming_birthdays(db, current_user.id)
