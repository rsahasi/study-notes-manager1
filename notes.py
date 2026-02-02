from __future__ import annotations
import db


def add_note(text: str) -> None:
    """Add a note (non-empty after stripping)."""
    cleaned = text.strip()
    if not cleaned:
        print("Note not added (empty)")
        return
    db.add_note_to_db(cleaned)
    print("Added")


def list_notes() -> None:
    """Print all notes with numbers."""
    notes = db.get_all_notes()
    if not notes:
        print("No notes yet")
        return

    for i, note in enumerate(notes, start=1):
        print(f"{i}. {note}")


def remove_note(note_num: str) -> bool:
    """Remove a note by number. Returns True if successful."""
    try:
        index = int(note_num)
        note_id = db.get_note_id_by_index(index)
        
        if note_id is None:
            notes = db.get_all_notes()
            if notes:
                print(f"Invalid number. Please enter a number between 1 and {len(notes)}")
            else:
                print("No notes to remove")
            return False
 
        notes_with_ids = db.get_all_notes_with_ids()
        note_text = next((text for nid, text, created_at in notes_with_ids if nid == note_id), "Unknown")
        
        if db.delete_note_by_id(note_id):
            print(f"Removed: {note_text}")
            return True
        else:
            print("Failed to remove note")
            return False
    except ValueError:
        print("Please enter a valid number")
        return False


db.init_db()
notes_count = len(db.get_all_notes())
if notes_count > 0:
    print(f"Loaded {notes_count} note(s) from database")
else:
    print("Starting new notes session")
while True:
    print("\nCommands: add, list, remove, quit")
    cmd = input("> ").strip().lower()
    if cmd == "add":
        text = input("Note: ")
        add_note(text)
    elif cmd == "list":
        list_notes()
    elif cmd == "remove":
        notes = db.get_all_notes()
        if notes:
            list_notes() 
            note_num = input("Enter note number to remove: ").strip()
            remove_note(note_num)
        else:
            print("No notes to remove")
    elif cmd in {"quit", "q", "exit"}:
        print("Thank you for using the notes app. Notes saved to database.")
        break
    else:
        print("Unknown command. Use: add, list, remove, quit")