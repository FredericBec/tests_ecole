# -*- coding: utf-8 -*-

"""
Classe Dao[Teacher]
"""

from models.teacher import Teacher
from models.address import Address
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class TeacherDao(Dao[Teacher]):
    def create(self, teacher: Teacher) -> int:
        """Crée en BD l'entité Teacher correspondant à l'enseignant teacher

        :param teacher: à créer sous forme d'entité Teacher en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        ...
        return 0

    @staticmethod
    def teacher_from_db(record) -> Teacher:
        """Construit un enseignant du modèle d'après son entité en BD"""
        teacher: Teacher = Teacher(record['first_name'], record['last_name'], record['age'], record['hiring_date'])
        teacher.id = record['id_teacher']

        if record['id_address'] is not None:
            teacher.address = \
                Address(record['street'], record['city'], record['postal_code'])
            teacher.address.id = record['id_address']

        return teacher

    def read(self, id_teacher: int) -> Optional[Teacher]:
        """Renvoit l'enseignant correspondant à l'entité dont l'id est id_teacher
           (ou None s'il n'a pu être trouvé)"""
        teacher: Optional[Teacher]

        with Dao.connection.cursor() as cursor:
            sql = """\
SELECT * FROM teacher T
INNER JOIN person P
ON T.id_person = P.id_person
LEFT JOIN address A
ON P.id_address = A.id_address
WHERE T.id_teacher = %s;"""
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()
        if record is not None:
            teacher = self.teacher_from_db(record)
        else:
            teacher = None

        return teacher

    def read_all(self) -> list[Teacher]:
        """Renvoit l'ensemble des enseignants de la BD."""
        teachers_list: list[Teacher] = []

        with Dao.connection.cursor() as cursor:
            sql = """\
SELECT * FROM teacher T
INNER JOIN person P
ON T.id_person = P.id_person
LEFT JOIN address A
ON P.id_address = A.id_address"""
            cursor.execute(sql)
            records = cursor.fetchall()
        for record in records:
            teachers_list.append(self.teacher_from_db(record))

        return teachers_list

    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité Teacher correspondant à teacher, pour y correspondre

        :param teacher: enseignant déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher

        :param teacher: enseignant dont l'entité Teacher correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True
