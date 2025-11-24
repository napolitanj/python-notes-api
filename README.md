# Python Notes API

A simple backend project built with **FastAPI**, **SQLAlchemy**, and **SQLite**.  
I built this to demonstrate core backend fundamentals: routing, schema validation, database models, CRUD operations, and dependency management.

## Features

- POST /notes — Create a note
- GET /notes — Read all notes
- DELETE /notes/{note_id} — Delete a note by ID
- PUT /notes/{note_id} — Update an existing note
- Automatic timestamps (created_at, updated_at)
- Sorting by date created or date updated
- Searching by text or category
- Retrieval by ID
- Pagination

## How to Run Locally

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Create the database tables
python
>>> from app.database import engine
>>> from app.models import Base
>>> Base.metadata.create_all(bind=engine)
>>> exit()

# Start the server
uvicorn app.main:app --reload
```
