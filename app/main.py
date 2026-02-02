import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import db

app = FastAPI()

class NoteCreate(BaseModel):
    text: str = Field(min_length=1)

class NoteOut(BaseModel):
    id: int
    text: str
    created_at: str

@app.on_event("startup")
def initialize_db():
    db.init_db()

@app.get("/notes", response_model=List[NoteOut])
def list_notes():
    row = db.get_all_notes_with_ids()
    return [{"id": r[0], "text": r[1], "created_at": r[2]} for r in row]

@app.post("/notes", response_model=NoteOut, status_code=201)
def create_note(note: NoteCreate):
    cleaned = note.text.strip()
    if cleaned:
        db.add_note_to_db(cleaned)
        notes = db.get_all_notes_with_ids()
        last_index = len(notes) - 1
        last = notes[last_index]
        return {"id": last[0], "text": last[1], "created_at": last[2]}
    else:
        raise HTTPException(status_code=400, detail="Note text cannot be empty")


@app.get("/notes/{id}", response_model=NoteOut)
def get_note(id: int):
    row = db.get_note_by_id(id)
    if not row:
        raise HTTPException(status_code=404, detail="Note not found")
    else:
        return{"id": row[0], "text": row[1], "created_at": row[2]}