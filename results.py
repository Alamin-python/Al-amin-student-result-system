"""results.py - Score calculation and grading logic."""

MIN_SUBJECTS = 5


def calculate_total(student):
    return sum(student.scores.values())


def calculate_average(student):
    """Average score, or 0.0 if the student has no scores yet."""
    if not student.scores:
        return 0.0
    return calculate_total(student) / len(student.scores)


def assign_grade(average):
    """Convert an average into a letter grade."""
    if average >= 70:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 40:
        return "D"
    return "F"


def remark(grade):
    remarks = {"A": "Excellent", "B": "Very Good", "C": "Good",
               "D": "Fair", "F": "Fail"}
    return remarks[grade]


def has_enough_subjects(student):
    return len(student.scores) >= MIN_SUBJECTS


def summary(student):
    """Return (total, average, grade) as a tuple."""
    avg = calculate_average(student)
    return calculate_total(student), avg, assign_grade(avg)
