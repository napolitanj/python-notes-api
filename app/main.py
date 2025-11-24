from fastapi import FastAPI, Depends, HTTPException
from .database import SessionLocal
from .schemas import NoteCreate, Note as NoteSchema
from sqlalchemy.orm import Session
from .models import Note as NoteModel

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Routes
@app.post("/notes", response_model=NoteSchema)
def add_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_update = NoteModel(text = note.text)
    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    return db_update

@app.get("/notes", response_model=list[NoteSchema])
def view_notes(db: Session = Depends(get_db)):
    return db.query(NoteModel).all()

@app.delete("/notes/{note_id}", response_model=NoteSchema)
def remove_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NoteModel).where(NoteModel.id == note_id).first()
    if note == None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
     db.delete(note)
     db.commit()
    return note

@app.put("/notes/{note_id}", response_model=NoteSchema)
def edit_note(note_id: int, new_note: NoteCreate, db: Session = Depends(get_db)):
    note= db.query(NoteModel).where(NoteModel.id == note_id).first()
    if note == None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        note.text = new_note.text
        db.commit()
        db.refresh(note)
    return note