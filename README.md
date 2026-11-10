# Student Result Management System

A menu-driven Python application for managing student records and results.

**Author:** Salihu Muhammad Al-amin
**Matric No:** 24/Sci01/194
**GitHub:** Alamin-python
**Course:** Introduction to Python Programming - New Horizon

## Features
- Add, view, search, update and delete students
- Record scores for 5+ subjects, update scores
- Automatic total, average and grade (A-F)
- Individual report cards
- Class listing sorted by average or name
- Class statistics (highest, lowest, class average)
- Text report export to a file
- JSON data persistence (data/students.json)

## How to run
Requires Python 3.8+ (standard library only, nothing to install).

```bash
git clone https://github.com/Alamin-python/Al-amin-student-result-system.git
cd Al-amin-student-result-system
python main.py
```

## Project structure
```
main.py       Entry point and menu
student.py    Student class + validation (regex, dates)
results.py    Totals, averages, grading
storage.py    Load/save JSON
reports.py    Report cards, sorting, statistics, export
data/         students.json is created here automatically
```

## Grading scale
| Average | Grade |
|---------|-------|
| 70-100  | A |
| 60-69   | B |
| 50-59   | C |
| 40-49   | D |
| 0-39    | F |

## Python concepts used
Variables and type conversion, if/elif/else, loops, lists/tuples/dictionaries,
functions, sorting (`sorted` with `key`), try/except/else/finally, file handling
(JSON), modules, OOP (Student class), `datetime`, `os`, `json`, `re`.
