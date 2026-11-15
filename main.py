"""main.py - menu-driven Student Study-Hours and Performance Dashboard."""
from pathlib import Path

import analysis
import visualization

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "data" / "students.csv"
GRAPHS_DIR = BASE_DIR / "graphs"
REPORTS_DIR = BASE_DIR / "reports"


def load_data():
    """Load the CSV and return a DataFrame (or None if loading failed)."""
    try:
        records, errors = analysis.read_student_records(CSV_PATH)
    except (FileNotFoundError, ValueError) as exc:
        print(f"\n[ERROR] {exc}")
        return None

    print(f"\nLoaded {len(records)} valid student records.")
    if errors:
        print(f"Skipped {len(errors)} invalid row(s):")
        for e in errors:
            print("  -", e)
    return analysis.records_to_dataframe(records)


def show_menu():
    print("\n" + "=" * 45)
    print("  STUDENT STUDY-HOURS & PERFORMANCE DASHBOARD")
    print("=" * 45)
    print("  1. Analyse student data (and save JSON report)")
    print("  2. Generate graphs")
    print("  3. View first 10 student records")
    print("  4. Exit")


def main():
    df = load_data()
    if df is None:
        return

    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            report = analysis.build_report(df)
            analysis.print_report(report)
            path = analysis.save_report_json(report, REPORTS_DIR)
            print(f"\nReport saved to: {path}")

        elif choice == "2":
            paths = visualization.generate_all_graphs(df, GRAPHS_DIR)
            print("\nGraphs created:")
            for p in paths:
                print("  -", p)

        elif choice == "3":
            print()
            print(df.head(10).to_string(index=False))

        elif choice == "4":
            print("\nThank you for using the dashboard. Goodbye!")
            break

        else:
            print("\n[!] Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()
