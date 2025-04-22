#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from business.school import School


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # initialisation statique d'un ensemble de cours, enseignants et élèves composant l'école
    school.init_static_school()

    # affichage de la liste des cours, leur enseignant et leurs élèves
    school.display_courses_list()

    School.test_get_entity_by_key()

    # initialisation depuis la BD d'un ensemble de cours, enseignants et élèves composant l'école
    school.init_from_db()

    # affichage de la liste des cours, leur enseignant et leurs élèves
    school.display_courses_list()


if __name__ == '__main__':
    main()
