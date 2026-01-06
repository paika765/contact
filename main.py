from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Models
class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str

class Contact(ContactCreate):
    id: int

# In-memory database
contacts: List[Contact] = []
id_counter = 1


# CREATE
@app.post("/contacts", response_model=Contact)
def create_contact(contact: ContactCreate):
    global id_counter
    new_contact = Contact(id=id_counter, **contact.dict())
    contacts.append(new_contact)
    id_counter += 1
    return new_contact


# READ ALL
@app.get("/contacts", response_model=List[Contact])
def get_contacts():
    return contacts


# READ ONE
@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: int):
    for contact in contacts:
        if contact.id == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")


# UPDATE
@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, updated: ContactCreate):
    for contact in contacts:
        if contact.id == contact_id:
            contact.name = updated.name
            contact.email = updated.email
            contact.phone = updated.phone
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")


# DELETE
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    for contact in contacts:
        if contact.id == contact_id:
            contacts.remove(contact)
            return {"message": "Contact deleted"}
    raise HTTPException(status_code=404, detail="Contact not found")
