from fastapi import FastAPI, Depends, HTTPException
from .database import SessionLocal
from .schemas import NoteCreate, NotePatch, Note as NoteSchema
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
def add_note(note: NoteCreate,  db: Session = Depends(get_db)):
    db_update = NoteModel(text = note.text, category = note.category)
    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    return db_update

@app.get("/notes", response_model=list[NoteSchema])
def view_notes(page: int = 1, limit: int = 20, sort: str | None = None, search: str | None = None, db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    notes = db.query(NoteModel)
    if search is not None:
        notes = notes.filter(NoteModel.text.contains(search) | NoteModel.category.contains(search))
    if sort == "created_at":
        notes = notes.order_by(NoteModel.created_at)
    elif sort == "updated_at":
        notes = notes.order_by(NoteModel.updated_at)
    notes = notes.offset(skip).limit(limit)
    return notes.all()

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

@app.patch("/notes/{note_id}", response_model=NoteSchema)
def patch_note(note_id: int, patch: NotePatch, db: Session = Depends(get_db)):
    note = db.query(NoteModel).where(NoteModel.id == note_id).first()
    if note == None:
        raise HTTPException(status_code=404, detail="Item not found")
    if patch.text is not None:
        note.text = patch.text
    if patch.category is not None:
        note.category = patch.category
    db.commit()
    db.refresh(note)
    return note