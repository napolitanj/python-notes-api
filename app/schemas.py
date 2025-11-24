from pydantic import BaseModel
from datetime import datetime


class NoteBase(BaseModel):
    text: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True