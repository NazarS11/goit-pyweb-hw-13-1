from sqlalchemy.orm import Session
from sqlalchemy import and_

from typing import List, Optional

from src.schemas import ContactCreate, ContactUpdate
from src.database.models import Contact, User
from datetime import datetime, timedelta

def create_contact(db: Session, contact: ContactCreate, user: User):
    db_contact = Contact(**contact.model_dump(), user_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, user: User, skip: int = 0, limit: int = 10):
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int, user: User):
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

def update_contact(db: Session, contact_id: int, contact: ContactUpdate, user: User):
    db_contact = get_contact(db, contact_id, user)
    if db_contact:
        for key, value in contact.model_dump().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, user: User):
    db_contact = get_contact(db, contact_id, user)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, user: User, query: Optional[str] = None):
    return db.query(Contact).filter(and_(
        (Contact.first_name.contains(query)) |
        (Contact.last_name.contains(query)) |
        (Contact.email.contains(query)) |
        (Contact.phone.contains(query))),Contact.user_id == user.id
    ).all()

def get_upcoming_birthdays(db: Session, user: User, days: int = 7):
    today = datetime.today().date()
    upcoming = today + timedelta(days=days)
    current_year = today.year
    upcoming_birthdays = []

    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in contacts:
        latest_birthday = contact.birthday.replace(year=current_year)
        if today <= latest_birthday <= upcoming:
            upcoming_birthdays.append(contact)
    
    return upcoming_birthdays

