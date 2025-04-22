# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""

from models.student import Student
from models.address import Address
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class StudentDao(Dao[Student]):
    def create(self, student: Student) -> int:
        """Crée en BD l'entité Student correspondant à l'étudiant student

        :param student: à créer sous forme d'entité Student en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        ...
        return 0

    @staticmethod
    def student_from_db(record) -> Student:
        """Construit un élève du modèle d'après son entité en BD"""
        student: Student = Student(record['first_name'], record['last_name'], record['age'])
        student.student_nbr = record['student_nbr']

        if record['id_address'] is not None:
            student.address = \
                Address(record['street'], record['city'], record['postal_code'])
            student.address.id = record['id_address']

        return student

    def read(self, student_nbr: int) -> Optional[Student]:
        """Renvoit l'élève correspondant à l'entité dont la clé primaire est student_nbr
           (ou None s'il n'a pu être trouvé)"""
        student: Optional[Student]

        with Dao.connection.cursor() as cursor:
            sql = """\
SELECT * FROM student S
INNER JOIN person P
ON S.id_person = P.id_person
LEFT JOIN address A
ON P.id_address = A.id_address
WHERE S.student_nbr = %s"""
            cursor.execute(sql, (student_nbr,))
            record = cursor.fetchone()
        if record is not None:
            student = self.student_from_db(record)
        else:
            student = None

        return student

    def read_all(self, id_course: Optional[int] = None) -> list[Student]:
        """Renvoit l'ensemble des élèves de la BD ou seulement ceux qui suivent
           le cours correspondant à l'entité dont l'id est id_course
           si ce paramètre est fourni."""
        students_list: list[Student] = []

        with Dao.connection.cursor() as cursor:
            sql = """\
SELECT * FROM student S
INNER JOIN person P
ON S.id_person = P.id_person
LEFT JOIN address A
ON P.id_address = A.id_address"""
            if id_course is None:
                cursor.execute(sql)
            else:
                sql += """
INNER JOIN takes TC
ON S.student_nbr = TC.student_nbr
WHERE id_course = %s"""
                cursor.execute(sql, (id_course,))
            records = cursor.fetchall()
        for record in records:
            students_list.append(self.student_from_db(record))

        return students_list

    def update(self, student: Student) -> bool:
        """Met à jour en BD l'entité Student correspondant à student, pour y correspondre

        :param student: élève déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, student: Student) -> bool:
        """Supprime en BD l'entité Student correspondant à student

        :param student: élève dont l'entité Student correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True
