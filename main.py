"""main.py - Entry point and menu for the Student Result Management System."""
from student import Student, is_valid_id, is_valid_date
from results import MIN_SUBJECTS, has_enough_subjects
import storage
import reports


def ask(prompt):
    return input(prompt).strip()


def ask_nonempty(prompt):
    while True:
        value = ask(prompt)
        if value:
            return value
        print("  This field cannot be empty.")


def ask_score(subject):
    """Keep asking until a valid score between 0 and 100 is entered."""
    while True:
        try:
            score = float(ask(f"  Score for {subject} (0-100): "))
        except ValueError:
            print("  Please enter a number.")
        else:
            if 0 <= score <= 100:
                return score
            print("  Score must be between 0 and 100.")


def ask_gender():
    while True:
        g = ask("Gender (M/F): ").upper()
        if g in ("M", "F"):
            return g
        print("  Enter M or F.")


def ask_dob():
    while True:
        dob = ask("Date of birth (YYYY-MM-DD): ")
        if is_valid_date(dob):
            return dob
        print("  Invalid date. Use the format YYYY-MM-DD, e.g. 2007-03-15.")


def find_student(students):
    """Ask for an ID and return the matching Student, or None."""
    student_id = ask("Enter Student ID: ")
    student = students.get(student_id)
    if student is None:
        print("  Student not found.")
    return student


# ---------- Student management ----------
def add_student(students):
    print("\n--- Add New Student ---")
    while True:
        student_id = ask("Student ID: ")
        if not is_valid_id(student_id):
            print("  Invalid ID (3-20 letters, digits, / - _ allowed).")
        elif student_id in students:
            print("  That ID already exists.")
        else:
            break
    name = ask_nonempty("Full name: ")
    student_class = ask_nonempty("Class/Form: ")
    gender = ask_gender()
    dob = ask_dob()
    students[student_id] = Student(student_id, name, student_class, gender, dob)
    storage.save_students(students)
    print(f"  Student '{name}' added.")


def view_students(students):
    print("\n--- All Students ---")
    if not students:
        print("  No students registered.")
        return
    print(f"{'ID':<14} {'Name':<26} {'Class':<8} {'G':<3} DOB")
    print("-" * 66)
    for s in students.values():
        print(s)


def search_students(students):
    term = ask("Search by ID or name: ").lower()
    matches = [s for s in students.values()
               if term in s.student_id.lower() or term in s.name.lower()]
    if not matches:
        print("  No matching students.")
    for s in matches:
        print(s)


def update_student(students):
    student = find_student(students)
    if student is None:
        return
    print("Press Enter to keep the current value.")
    student.name = ask(f"Name [{student.name}]: ") or student.name
    student.student_class = ask(f"Class [{student.student_class}]: ") or student.student_class
    gender = ask(f"Gender [{student.gender}]: ").upper()
    if gender in ("M", "F"):
        student.gender = gender
    dob = ask(f"DOB [{student.dob}]: ")
    if dob and is_valid_date(dob):
        student.dob = dob
    elif dob:
        print("  Invalid date ignored.")
    storage.save_students(students)
    print("  Student updated.")


def delete_student(students):
    student = find_student(students)
    if student is None:
        return
    if ask(f"Delete {student.name}? (y/n): ").lower() == "y":
        del students[student.student_id]
        storage.save_students(students)
        print("  Student deleted.")


# ---------- Score management ----------
def record_scores(students):
    student = find_student(students)
    if student is None:
        return
    print(f"Enter at least {MIN_SUBJECTS} subjects for {student.name}.")
    count = 0
    while True:
        subject = ask("Subject name (blank to finish): ").title()
        if not subject:
            if count < MIN_SUBJECTS and not has_enough_subjects(student):
                print(f"  You still need at least {MIN_SUBJECTS} subjects.")
                continue
            break
        student.set_score(subject, ask_score(subject))
        count += 1
    storage.save_students(students)
    print("  Scores saved.")


def update_score(students):
    student = find_student(students)
    if student is None:
        return
    if not student.scores:
        print("  This student has no scores yet.")
        return
    print("Current subjects:", ", ".join(student.scores))
    subject = ask("Subject to update: ").title()
    if subject not in student.scores:
        print("  Subject not found.")
        return
    student.set_score(subject, ask_score(subject))
    storage.save_students(students)
    print("  Score updated.")


def show_report_card(students):
    student = find_student(students)
    if student is None:
        return
    if not student.scores:
        print("  No scores recorded for this student.")
        return
    print(reports.report_card(student))


# ---------- Reports ----------
def list_results(students):
    if not students:
        print("  No students registered.")
        return
    choice = ask("Sort by (1) average or (2) name: ")
    by = "name" if choice == "2" else "average"
    print(reports.results_table(reports.sort_students(list(students.values()), by)))


def show_statistics(students):
    print(reports.format_statistics(reports.class_statistics(list(students.values()))))


def export_report(students):
    path = reports.save_report(list(students.values()))
    if path:
        print(f"  Report saved to: {path}")


MENU = """
===== STUDENT RESULT MANAGEMENT SYSTEM =====
 1. Add student              8. Show report card
 2. View all students        9. List results (sorted)
 3. Search student          10. Class statistics
 4. Update student          11. Save report to file
 5. Delete student           0. Exit
 6. Record scores
 7. Update a score
"""


def main():
    students = storage.load_students()
    actions = {
        "1": add_student, "2": view_students, "3": search_students,
        "4": update_student, "5": delete_student, "6": record_scores,
        "7": update_score, "8": show_report_card, "9": list_results,
        "10": show_statistics, "11": export_report,
    }
    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        if choice == "0":
            storage.save_students(students)
            print("Data saved. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            try:
                action(students)
            except (KeyboardInterrupt, EOFError):
                print("\n  Cancelled.")
        else:
            print("  Invalid option, try again.")


if __name__ == "__main__":
    main()
