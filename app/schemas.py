from pydantic import BaseModel
from datetime import datetime


class NoteBase(BaseModel):
    text: str
    category: str

class NoteCreate(NoteBase):
    pass

class NotePatch(NoteBase):
    text: str | None = None
    category: str | None = None

class Note(NoteBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True