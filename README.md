# Student Study-Hours and Performance Dashboard

A beginner-friendly Python data analysis project that studies the relationship
between students' daily study hours and their examination marks.

## Features
- CSV dataset of simulated, anonymised student records
- `StudentRecord` class (OOP) with input validation
- NumPy statistics: total, mean hours, mean marks, highest, lowest, correlation
- Pandas course-wise performance analysis
- 3 Matplotlib graphs: scatter plot, histogram, bar chart
- Menu-driven interface
- JSON reports saved with a timestamp
- Error handling for missing files, missing columns and bad rows

## Project structure
```
student_dashboard/
├── main.py             # menu-driven application
├── student.py          # StudentRecord class
├── analysis.py         # reading data, statistics, JSON reports
├── visualization.py    # Matplotlib graphs
├── generate_data.py    # creates the sample dataset
├── requirements.txt
├── data/students.csv
├── graphs/             # generated PNG graphs
└── reports/            # generated JSON reports
```

## How to run (VS Code, Python 3.13)
1. Open the `student_dashboard` folder in VS Code.
2. Open a terminal (Ctrl + `) and install libraries:
   `pip install -r requirements.txt`
3. (Optional) Re-create the dataset: `python generate_data.py`
4. Run the app: `python main.py`
5. Choose option 1 for analysis, 2 for graphs, 4 to exit.

## Note
Correlation shows association only. It does not prove that more study time
directly causes higher marks.
