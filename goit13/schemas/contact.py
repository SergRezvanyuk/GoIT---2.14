from pydantic import BaseModel
from datetime import date

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date
    additional_data: str | None = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
