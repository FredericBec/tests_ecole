# -*- coding: utf-8 -*-

"""
Classe School
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from daos.teacher_dao import TeacherDao
from daos.student_dao import StudentDao
from daos.course_dao import CourseDao
from models.address import Address
from models.course import Course
from models.teacher import Teacher
from models.student import Student


@dataclass
class School:
    """Couche métier de l'application de gestion d'une école,
    reprenant les cas d'utilisation et les spécifications fonctionnelles :
    - courses : liste des cours existants
    - teachers : liste des enseignants
    - students : liste des élèves"""

    courses: list[Course] = field(default_factory=list, init=False)
    teachers: list[Teacher] = field(default_factory=list, init=False)
    students: list[Student] = field(default_factory=list, init=False)

    def add_course(self, course: Course) -> None:
        """Ajout du cours course à la liste des cours."""
        self.courses.append(course)

    def add_teacher(self, teacher: Teacher) -> None:
        """Ajout de l'enseignant teacher à la liste des enseignants."""
        self.teachers.append(teacher)

    def add_student(self, student: Student) -> None:
        """Ajout de l'élève spécifié à la liste des élèves."""
        self.students.append(student)

    def display_courses_list(self) -> None:
        """Affichage de la liste des cours avec pour chacun d'eux :
        - leur enseignant
        - la liste des élèves le suivant"""
        for course in self.courses:
            print(f"cours de {course}")
            for student in course.students_taking_it:
                print(f"- {student}")
            print()

    @staticmethod
    def get_teacher_by_id(id_teacher: int) -> Optional[Teacher]:
        teacher_dao: TeacherDao = TeacherDao()
        return teacher_dao.read(id_teacher)

    @staticmethod
    def get_student_by_nbr(student_nbr: int) -> Optional[Student]:
        student_dao: StudentDao = StudentDao()
        return student_dao.read(student_nbr)

    @staticmethod
    def get_course_by_id(id_course: int) -> Optional[Course]:
        course_dao: CourseDao = CourseDao()
        return course_dao.read(id_course)

    @classmethod
    def test_get_entity_by_key(cls) -> None:
        print('===')
        course_1 = cls.get_course_by_id(1)
        if course_1 is not None:
            print(f"{course_1}\n{course_1.students_taking_it}")
        course_2 = cls.get_course_by_id(2)
        if course_2 is not None:
            print(f"{course_2}\n{course_2.students_taking_it}")
        print(cls.get_course_by_id(9))
        print('---')
        print(cls.get_teacher_by_id(1))
        print(cls.get_teacher_by_id(2))
        print(cls.get_teacher_by_id(9))
        print('---')
        student_1 = cls.get_student_by_nbr(1)
        if student_1 is not None:
            print(f"{student_1}\n{student_1.courses_taken}")
        student_2 = cls.get_student_by_nbr(2)
        if student_2 is not None:
            print(f"{student_2}\n{student_2.courses_taken}")
        print(cls.get_student_by_nbr(9))
        print('===')

    def init_from_db(self) -> None:
        """Initialisation de l'école depuis la base de données"""
        teacher_dao: TeacherDao = TeacherDao()
        student_dao: StudentDao = StudentDao()
        course_dao: CourseDao = CourseDao()

        # récupérations de l'ensemble des enseignants
        self.teachers = teacher_dao.read_all()

        # récupérations de l'ensemble des étudiants et construction d'un dictionnaire
        # permettant de récupérer chaque élève selon son id
        self.students = student_dao.read_all()
        student_by_nbr: dict[int, Student] = {student.student_nbr: student for student in self.students}

        # récupérations de l'ensemble des cours
        self.courses = course_dao.read_all()

        # association à chaque cours des élèves le suivant et à chaque élève des cours qu'il suit
        course: Course
        student: Student
        for course in self.courses:
            course.students_taking_it = \
                [student_by_nbr[student.student_nbr] for student in student_dao.read_all(course.id)]
            for student in course.students_taking_it:
                student.courses_taken.append(course)

    def init_static_school(self) -> None:
        """Initialisation d'un jeu de test pour l'école self."""

        # création des étudiants et rattachement à leur adresse
        paul: Student    = Student('Paul', 'Dubois', 12)
        valerie: Student = Student('Valérie', 'Dumont', 13)
        louis: Student   = Student('Louis', 'Berthot', 11)

        paul.address    = Address('12 rue des Pinsons', 'Castanet', 31320)
        valerie.address = Address('43 avenue Jean Zay', 'Toulouse', 31200)
        louis.address   = Address('7 impasse des Coteaux', 'Cornebarrieu', 31150)

        # ajout de ceux-ci à l'école
        for student in [paul, valerie, louis]:
            self.add_student(student)

        # création des cours
        francais: Course = Course("Français", date(2024, 1, 29),
                                              date(2024, 2, 16))
        histoire: Course = Course("Histoire", date(2024, 2, 5),
                                              date(2024, 2, 16))
        geographie: Course = Course("Géographie", date(2024, 2, 5),
                                                  date(2024, 2, 16))
        mathematiques: Course = Course("Mathématiques", date(2024, 2, 12),
                                                        date(2024, 3, 8))
        physique: Course = Course("Physique", date(2024, 2, 19),
                                              date(2024, 3, 8))
        chimie: Course = Course("Chimie", date(2024, 2, 26),
                                          date(2024, 3, 15))
        anglais: Course = Course("Anglais", date(2024, 2, 12),
                                            date(2024, 2, 24))
        sport: Course = Course("Sport", date(2024, 3, 4),
                                        date(2024, 3, 15))

        # ajout de ceux-ci à l'école
        for course in [francais, histoire, geographie, mathematiques,
                       physique, chimie, anglais, sport]:
            self.add_course(course)

        # création des enseignants
        victor  = Teacher('Victor', 'Hugo', 23, date(2023, 9, 4))
        jules   = Teacher('Jules', 'Michelet', 32, date(2023, 9, 4))
        sophie  = Teacher('Sophie', 'Germain', 25, date(2023, 9, 4))
        marie   = Teacher('Marie', 'Curie', 31, date(2023, 9, 4))
        william = Teacher('William', 'Shakespeare', 34, date(2023, 9, 4))
        michel  = Teacher('Michel', 'Platini', 42, date(2023, 9, 4))

        # ajout de ceux-ci à l'école
        for teacher in [victor, jules, sophie, marie, william, michel]:
            self.add_teacher(teacher)

        # association des élèves aux cours qu'ils suivent
        for course in [geographie, physique, anglais]:
            paul.add_course(course)

        for course in [francais, histoire, chimie]:
            valerie.add_course(course)

        for course in [mathematiques, physique, geographie, sport]:
            louis.add_course(course)

        # association des enseignants aux cours qu'ils enseignent
        victor.add_course(francais)

        jules.add_course(histoire)
        jules.add_course(geographie)

        sophie.add_course(mathematiques)

        marie.add_course(physique)
        marie.add_course(chimie)

        william.add_course(anglais)

        michel.add_course(sport)
