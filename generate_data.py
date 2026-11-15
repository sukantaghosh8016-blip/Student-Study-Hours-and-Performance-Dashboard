"""Generates a simulated, anonymised dataset (data/students.csv).

Run once:  python generate_data.py
No real student information is used.
"""
import csv
import random
from pathlib import Path

random.seed(42)
COURSES = ["Computer Science", "Mathematics", "Physics", "Commerce", "English"]
# Small course-level offset so the course-wise comparison is interesting
OFFSET = {"Computer Science": 4, "Mathematics": 2, "Physics": -2,
          "Commerce": 0, "English": 3}

rows = []
for i in range(1, 61):
    course = random.choice(COURSES)
    hours = round(random.uniform(0.5, 7.5), 1)
    marks = 30 + 7.0 * hours + OFFSET[course] + random.gauss(0, 6)
    marks = int(max(0, min(100, round(marks))))
    rows.append([f"S{i:03d}", course, hours, marks])

out = Path(__file__).parent / "data" / "students.csv"
out.parent.mkdir(exist_ok=True)
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["student_id", "course", "study_hours", "marks"])
    w.writerows(rows)
print(f"Created {out} with {len(rows)} records.")
