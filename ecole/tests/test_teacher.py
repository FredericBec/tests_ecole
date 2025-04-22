import datetime

from models.course import Course
from models.teacher import Teacher


def test_teacher_str():
    teacher = Teacher("Morgane", "Lafee", 45, datetime.date(1995, 5, 20))

    expected_value = "Morgane Lafee (45 ans), arrivé(e) le 1995-05-20"

    assert str(teacher) == expected_value


def test_add_course():
    teacher = Teacher("Robert", "De niro", 50, datetime.date(2000, 12, 1))
    course = Course("Cinéma", datetime.date(2000, 12, 5), datetime.date(2020, 5, 6))

    teacher.add_course(course)

    assert course.teacher == teacher
