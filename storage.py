"""storage.py - Load and save data using JSON."""
import json
import os

from student import Student

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students(path=DATA_FILE):
    """Load students from JSON. Returns {} if the file is missing or damaged."""
    students = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print("No data file found yet - starting with an empty system.")
        return students
    except json.JSONDecodeError:
        print("Warning: data file is corrupted. Starting with an empty system.")
        return students
    else:
        for item in raw:
            student = Student.from_dict(item)
            students[student.student_id] = student
        return students
    finally:
        pass  # nothing to clean up; 'with' already closed the file


def save_students(students, path=DATA_FILE):
    """Write all students to JSON. Returns True on success."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students.values()], f, indent=4)
        return True
    except OSError as error:
        print(f"Error saving data: {error}")
        return False
