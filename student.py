"""student.py - the StudentRecord class (Object-Oriented Programming)."""


class StudentRecord:
    """Stores the details of one student."""

    def __init__(self, student_id, course, study_hours, marks):
        self.student_id = str(student_id).strip()
        self.course = str(course).strip()
        self.study_hours = float(study_hours)
        self.marks = float(marks)
        self.validate()

    def validate(self):
        """Raise ValueError if any field is invalid."""
        if not self.student_id:
            raise ValueError("Student ID is missing.")
        if not self.course:
            raise ValueError("Course name is missing.")
        if not 0 <= self.study_hours <= 24:
            raise ValueError(f"Study hours must be between 0 and 24 "
                             f"(got {self.study_hours}).")
        if not 0 <= self.marks <= 100:
            raise ValueError(f"Marks must be between 0 and 100 "
                             f"(got {self.marks}).")

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "course": self.course,
            "study_hours": self.study_hours,
            "marks": self.marks,
        }

    def __str__(self):
        return (f"{self.student_id} | {self.course} | "
                f"{self.study_hours} h/day | {self.marks} marks")

    def __repr__(self):
        return (f"StudentRecord({self.student_id!r}, {self.course!r}, "
                f"{self.study_hours}, {self.marks})")
