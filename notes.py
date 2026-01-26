from __future__ import annotations
from datetime import datetime
import os
def add_note(notes: list[str], text: str) -> None:
    """Add a note (non-empty after stripping)."""
    cleaned = text.strip()
    if not cleaned:
        print("Note not added (empty)")
        return
    notes.append(cleaned)
    print("Added")


def list_notes(notes: list[str]) -> None:
    """Print all notes with numbers."""
    if not notes:
        print("No notes yet")
        return

    for i, note in enumerate(notes, start=1):
        print(f"{i}. {note}")


def remove_note(notes: list[str], note_num: str) -> bool:
    """Remove a note by number. Returns True if successful."""
    if not notes:
        print("No notes to remove")
        return False
    
    try:
        index = int(note_num) - 1  
        if 0 <= index < len(notes):
            removed = notes.pop(index)
            print(f"Removed: {removed}")
            return True
        else:
            print(f"Invalid number. Please enter a number between 1 and {len(notes)}")
            return False
    except ValueError:
        print("Please enter a valid number")
        return False


def generate_filename() -> str:
    """Generate a unique filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"notes_{timestamp}.txt"


def save_notes(notes: list[str], filename: str) -> None:
    """Save notes to file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for note in notes:
                f.write(note + '\n')
        print(f"Notes saved to {filename}")
    except Exception as e:
        print(f"Error saving notes: {e}")


def load_notes(filename: str) -> list[str]:
    """Load notes from file if it exists."""
    notes = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                notes = [line.strip() for line in f if line.strip()]
            print(f"Loaded {len(notes)} note(s) from {filename}")
        except Exception as e:
            print(f"Error loading notes: {e}")
    else:
        print(f"Starting new notes session: {filename}")
    return notes


session_filename = generate_filename()
notes = load_notes(session_filename)
while True:
    print("\nCommands: add, list, remove, quit")
    cmd = input("> ").strip().lower()
    if cmd == "add":
        text = input("Note: ")
        add_note(notes, text)
        save_notes(notes, session_filename)
    elif cmd == "list":
        list_notes(notes)
    elif cmd == "remove":
        if notes:
            list_notes(notes)  # Show notes first
            note_num = input("Enter note number to remove: ").strip()
            if remove_note(notes, note_num):
                save_notes(notes, session_filename)
        else:
            print("No notes to remove")
    elif cmd in {"quit", "q", "exit"}:
        save_notes(notes, session_filename)
        print(f"Thank you for using the notes app. Notes saved to {session_filename}")
        break
    else:
        print("Unknown command. Use: add, list, remove, quit")