import datetime

from models.course import Course
from models.student import Student


def test_student_str():
    student = Student("Toto", "Zero", 11)

    expected_value = "Toto Zero (11 ans), n° étudiant : 1"

    assert str(student) == expected_value


def test_add_course():
    student = Student("tarti", "flette", 14)
    course = Course("maths", datetime.date.today(), datetime.date.today())

    student.add_course(course)

    assert student.courses_taken == [course]
