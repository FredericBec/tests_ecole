# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""

from dataclasses import dataclass
from typing import Optional
from models.course import Course
from daos.dao import Dao
from daos.teacher_dao import TeacherDao


@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours course

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        ...
        return 0

    @staticmethod
    def course_from_db(record) -> Course:
        """Construit un cours du modèle d'après son entité en BD"""
        course: Course = Course(record['name'], record['start_date'], record['end_date'])
        course.id = record['id_course']

        id_teacher = record['id_teacher']
        if id_teacher is not None:
            course.teacher = TeacherDao().read(id_teacher)

        return course

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
        if record is not None:
            course = self.course_from_db(record)
        else:
            course = None

        return course

    def read_all(self) -> list[Course]:
        """Renvoit l'ensemble des cours de la BD."""
        courses_list: list[Course] = []

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course"
            cursor.execute(sql)
            records = cursor.fetchall()
        for record in records:
            courses_list.append(self.course_from_db(record))

        return courses_list

    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True
