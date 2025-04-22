import datetime

from models.course import Course
from models.student import Student
from models.teacher import Teacher


def test_course_str():
    course = Course("Physique - chimie", datetime.date(2025,1,20), datetime.date(2025, 12, 12))

    expected_value = "Physique - chimie (2025-01-20 – 2025-12-12),\npas d'enseignant affecté"

    assert str(course) == expected_value


def test_add_student():
    course = Course("geo", datetime.date.today(), datetime.date.today())
    student = Student("Martin", "Matin", 13)

    course.add_student(student)

    assert course.students_taking_it == [student]


def test_set_teacher():
    course = Course("français", datetime.date.today(), datetime.date.today())
    teacher = Teacher("Gilbert", "Montagné", 35, datetime.date.today())

    course.set_teacher(teacher)

    assert teacher.courses_teached == [course]
