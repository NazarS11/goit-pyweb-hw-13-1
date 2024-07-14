from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_limiter.depends import RateLimiter

from src.schemas import Contact, ContactCreate, ContactUpdate
from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as contact_repository
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/search/", response_model=List[Contact])
def search_contacts(query: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return contact_repository.search_contacts(db, current_user, query=query)

@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db),current_user: User = Depends(auth_service.get_current_user)):
    return contact_repository.create_contact(db, contact, current_user)

@router.get("/", response_model=List[Contact], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return contact_repository.get_contacts(db, current_user, skip=skip, limit=limit)

@router.get("/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db),current_user: User = Depends(auth_service.get_current_user)):
    db_contact = contact_repository.get_contact(db, contact_id, current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    db_contact = contact_repository.update_contact(db, contact_id, contact, current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    db_contact = contact_repository.delete_contact(db, contact_id, current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/birthdays/", response_model=List[Contact])
def upcoming_birthdays(db: Session = Depends(get_db), days: int = 7, current_user: User = Depends(auth_service.get_current_user)):
    return contact_repository.get_upcoming_birthdays(db, current_user, days=days)
