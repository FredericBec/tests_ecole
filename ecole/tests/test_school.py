import datetime
from unittest.mock import patch, MagicMock, Mock

import pytest

from business.school import School
from models.course import Course
from models.student import Student
from models.teacher import Teacher


@pytest.fixture
def mock_dao_connection():
    with patch('daos.dao.pymysql.connect') as mock_connect:
        mock_conn = MagicMock()
        cursor = MagicMock()

        mock_connect.return_value.cursor.return_value.__enter__.return_value = cursor
        mock_connect.return_value = mock_conn

        yield {
            'mock_connect': mock_connect,
            'mock_conn': mock_conn,
            'cursor': cursor
        }


def test_get_teacher(mock_dao_connection, mocker):
    teacher = Teacher("Robert", "De niro", 50, datetime.date(2000, 12, 1))
    mocker.patch.object(School, 'get_teacher_by_id', return_value=teacher)

    expected_teacher = Teacher("Robert", "De niro", 50, datetime.date(2000, 12, 1))

    assert School.get_teacher_by_id(1) == expected_teacher


def test_get_student(mock_dao_connection, mocker):
    student = Student("Toto", "Zero", 11)
    mocker.patch.object(School, 'get_student_by_nbr', return_value=student)

    expected_student = Student("Toto", "Zero", 11)

    assert School.get_student_by_nbr(1).first_name == expected_student.first_name
    assert School.get_student_by_nbr(1).last_name == expected_student.last_name
    assert School.get_student_by_nbr(1).age == expected_student.age


def test_get_course(mock_dao_connection, mocker):
    course = Course("maths", datetime.date(2000, 2, 26), datetime.date(2001, 2, 18))
    mocker.patch.object(School, 'get_course_by_id', return_value=course)

    expected_course = Course("maths", datetime.date(2000, 2, 26), datetime.date(2001, 2, 18))

    assert School.get_course_by_id(1) == expected_course
