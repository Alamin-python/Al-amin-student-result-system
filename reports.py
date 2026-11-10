"""reports.py - Listing, sorting, statistics and report generation."""
import os
from datetime import datetime

from results import summary, calculate_average, remark

REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def report_card(student):
    """Return a formatted report card for one student as a string."""
    total, avg, grade = summary(student)
    lines = [
        "=" * 50,
        "              STUDENT REPORT CARD",
        "=" * 50,
        f"Name      : {student.name}",
        f"ID        : {student.student_id}",
        f"Class     : {student.student_class}",
        f"Gender    : {student.gender}",
        f"Date Born : {student.dob}",
        f"Entered   : {student.date_entered or 'N/A'}",
        "-" * 50,
        f"{'Subject':<30}{'Score':>10}",
        "-" * 50,
    ]
    for subject, score in student.scores.items():
        lines.append(f"{subject:<30}{score:>10.1f}")
    lines += [
        "-" * 50,
        f"Total   : {total:.1f}",
        f"Average : {avg:.2f}",
        f"Grade   : {grade} ({remark(grade)})",
        "=" * 50,
    ]
    return "\n".join(lines)


def sort_students(students, by="average"):
    """Return a sorted list: by 'average' (high to low) or 'name' (A-Z)."""
    if by == "name":
        return sorted(students, key=lambda s: s.name.lower())
    return sorted(students, key=calculate_average, reverse=True)


def results_table(students):
    """Return a table of students with total, average and grade."""
    header = (f"{'Pos':<5}{'ID':<14}{'Name':<26}{'Total':>8}{'Average':>10}{'Grade':>7}")
    lines = [header, "-" * len(header)]
    for position, s in enumerate(students, start=1):
        total, avg, grade = summary(s)
        lines.append(f"{position:<5}{s.student_id:<14}{s.name:<26}"
                     f"{total:>8.1f}{avg:>10.2f}{grade:>7}")
    return "\n".join(lines)


def class_statistics(students):
    """Return a dict of class stats, or None if no student has scores."""
    scored = [s for s in students if s.scores]
    if not scored:
        return None
    averages = [calculate_average(s) for s in scored]
    all_scores = [score for s in scored for score in s.scores.values()]
    best = max(scored, key=calculate_average)
    worst = min(scored, key=calculate_average)
    return {
        "students": len(scored),
        "highest_score": max(all_scores),
        "lowest_score": min(all_scores),
        "class_average": sum(averages) / len(averages),
        "top_student": best.name,
        "bottom_student": worst.name,
    }


def format_statistics(stats):
    if stats is None:
        return "No scores recorded yet."
    return "\n".join([
        f"Students with scores : {stats['students']}",
        f"Highest single score : {stats['highest_score']:.1f}",
        f"Lowest single score  : {stats['lowest_score']:.1f}",
        f"Class average        : {stats['class_average']:.2f}",
        f"Top student          : {stats['top_student']}",
        f"Lowest student       : {stats['bottom_student']}",
    ])


def full_report(students):
    """Build the full class report text."""
    ranked = sort_students(students, "average")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "\n".join([
        "STUDENT RESULT MANAGEMENT SYSTEM - CLASS REPORT",
        f"Generated: {now}",
        "",
        results_table(ranked),
        "",
        "CLASS STATISTICS",
        "-" * 30,
        format_statistics(class_statistics(students)),
    ])


def save_report(students, filename=None):
    """Save the full report to a text file. Returns the file path, or None on error."""
    if filename is None:
        filename = "report_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    path = os.path.join(REPORT_DIR, filename)
    try:
        os.makedirs(REPORT_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(full_report(students))
        return path
    except OSError as error:
        print(f"Could not save report: {error}")
        return None
