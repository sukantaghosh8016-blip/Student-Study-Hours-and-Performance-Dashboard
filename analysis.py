"""analysis.py - reading records, statistics and report generation."""
import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from student import StudentRecord

REQUIRED_COLUMNS = ["student_id", "course", "study_hours", "marks"]


def read_student_records(csv_path):
    """Read the CSV file and return (records, errors).

    Invalid rows are skipped and described in `errors`, so one bad row
    does not stop the whole program.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}. "
                                f"Run generate_data.py first.")

    records, errors = [], []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS
                   if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"CSV is missing column(s): {', '.join(missing)}")

        for line_no, row in enumerate(reader, start=2):
            try:
                records.append(StudentRecord(row["student_id"], row["course"],
                                             row["study_hours"], row["marks"]))
            except (ValueError, TypeError) as exc:
                errors.append(f"Line {line_no}: {exc}")

    if not records:
        raise ValueError("No valid student records were found.")
    return records, errors


def records_to_dataframe(records):
    """Convert a list of StudentRecord objects into a Pandas DataFrame."""
    return pd.DataFrame([r.to_dict() for r in records])


def calculate_statistics(df):
    """Overall statistics using NumPy."""
    hours = df["study_hours"].to_numpy()
    marks = df["marks"].to_numpy()

    if len(df) > 1 and hours.std() > 0 and marks.std() > 0:
        correlation = float(np.corrcoef(hours, marks)[0, 1])
    else:
        correlation = None  # cannot be calculated

    return {
        "total_students": int(len(df)),
        "average_study_hours": round(float(np.mean(hours)), 2),
        "average_marks": round(float(np.mean(marks)), 2),
        "highest_marks": float(np.max(marks)),
        "lowest_marks": float(np.min(marks)),
        "correlation": None if correlation is None else round(correlation, 3),
        "correlation_meaning": interpret_correlation(correlation),
    }


def interpret_correlation(r):
    """Describe the correlation coefficient in plain English."""
    if r is None:
        return "Correlation could not be calculated."
    strength = abs(r)
    if strength >= 0.7:
        label = "strong"
    elif strength >= 0.4:
        label = "moderate"
    elif strength >= 0.2:
        label = "weak"
    else:
        return "Little or no linear relationship."
    direction = "positive" if r > 0 else "negative"
    return (f"A {label} {direction} relationship. Note: correlation does "
            f"not prove that extra study time causes higher marks.")


def course_wise_analysis(df):
    """Average hours, average marks and count for every course."""
    grouped = (df.groupby("course")
                 .agg(students=("student_id", "count"),
                      average_study_hours=("study_hours", "mean"),
                      average_marks=("marks", "mean"))
                 .round(2)
                 .sort_values("average_marks", ascending=False))
    return grouped


def build_report(df):
    """Combine all results into one dictionary."""
    course_table = course_wise_analysis(df)
    return {
        "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "overall_statistics": calculate_statistics(df),
        "course_wise_performance": course_table.reset_index()
                                               .to_dict(orient="records"),
    }


def save_report_json(report, reports_dir):
    """Save the report as a time-stamped JSON file and return its path."""
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(exist_ok=True)
    name = f"analysis_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    path = reports_dir / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    return path


def print_report(report):
    """Print the report in a readable form."""
    s = report["overall_statistics"]
    print("\n" + "=" * 55)
    print("  STUDENT STUDY-HOURS AND PERFORMANCE REPORT")
    print("=" * 55)
    print(f"  Total students        : {s['total_students']}")
    print(f"  Average study hours   : {s['average_study_hours']} h/day")
    print(f"  Average marks         : {s['average_marks']}")
    print(f"  Highest marks         : {s['highest_marks']}")
    print(f"  Lowest marks          : {s['lowest_marks']}")
    print(f"  Correlation (r)       : {s['correlation']}")
    print(f"  Meaning               : {s['correlation_meaning']}")
    print("-" * 55)
    print("  Course-wise performance")
    print(f"  {'Course':<18}{'Students':>9}{'Avg Hrs':>9}{'Avg Marks':>11}")
    for row in report["course_wise_performance"]:
        print(f"  {row['course']:<18}{row['students']:>9}"
              f"{row['average_study_hours']:>9}{row['average_marks']:>11}")
    print("=" * 55)
