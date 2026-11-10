"""student.py - Student class and validation helpers."""
import re
from datetime import datetime

ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9/_-]{2,19}$")
DATE_FORMAT = "%Y-%m-%d"


def is_valid_id(student_id):
    """Return True if the student ID looks valid (e.g. STU001 or 24/Sci01/194)."""
    return bool(ID_PATTERN.match(student_id))


def is_valid_date(text):
    """Return True if text is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(text, DATE_FORMAT)
        return True
    except ValueError:
        return False


class Student:
    """Represents one student and their subject scores."""

    def __init__(self, student_id, name, student_class, gender, dob,
                 scores=None, date_entered=None):
        self.student_id = student_id
        self.name = name
        self.student_class = student_class
        self.gender = gender
        self.dob = dob
        self.scores = scores if scores is not None else {}   # {subject: score}
        self.date_entered = date_entered                     # when scores were recorded

    def set_score(self, subject, score):
        """Record or update a subject score and stamp the date/time."""
        self.scores[subject] = float(score)
        self.date_entered = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "student_class": self.student_class,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "date_entered": self.date_entered,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["student_id"], data["name"], data["student_class"],
            data["gender"], data["dob"],
            data.get("scores", {}), data.get("date_entered"),
        )

    def __str__(self):
        return (f"{self.student_id:<14} {self.name:<26} {self.student_class:<8} "
                f"{self.gender:<3} {self.dob}")
