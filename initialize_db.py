import os
import django

from users.models import Student, Professor
from grades.models import Subject, Course, Inscription, CourseInscription, Restriction

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'university_califications.settings')
django.setup()


def initialize_db():
    print('Initializing database...')

    student01 = Student.objects.create(
        username='student01',
        first_name='Juan',
        last_name='Perez',
        password='axBc%1234',
    )

    student02 = Student.objects.create(
        username='student02',
        first_name='Maria',
        last_name='Gomez',
        password='zXyT%1234',
    )

    student03 = Student.objects.create(
        username='student03',
        first_name='Carlos',
        last_name='Rodriguez',
        password='qWeR%1234',
    )

    student04 = Student.objects.create(
        username='student04',
        first_name='Ana',
        last_name='Martinez',
        password='pLoK%1234',
    )

    professor01 = Professor.objects.create(
        username='professor01',
        first_name='Pedro',
        last_name='Garcia',
        password='mNoP%1234',
    )

    professor02 = Professor.objects.create(
        username='professor02',
        first_name='Luis',
        last_name='Hernandez',
        password='kJhG%1234',
    )

    professor03 = Professor.objects.create(
        username='professor03',
        first_name='Laura',
        last_name='Diaz',
        password='iJkL%1234',
    )

    professor04 = Professor.objects.create(
        username='professor04',
        first_name='Sofia',
        last_name='Sanchez',
        password='hKlM%1234',
    )

    subject01 = Subject.objects.create(
        name='Math',
        credits=4,
    )

    subject02 = Subject.objects.create(
        name='Math II',
        credits=4,
    )

    subject03 = Subject.objects.create(
        name='Physics',
        credits=3,
    )

    subject04 = Subject.objects.create(
        name='Physics II',
        credits=3,
    )

    subject05 = Subject.objects.create(
        name='Chemistry',
        credits=2,
    )

    subject06 = Subject.objects.create(
        name='Biology',
        credits=3,
    )

    subject07 = Subject.objects.create(
        name='History',
        credits=2,
    )

    subject08 = Subject.objects.create(
        name='Geography',
        credits=2,
    )

    subject09 = Subject.objects.create(
        name='Literature',
        credits=3,
    )

    subject10 = Subject.objects.create(
        name='Physics III',
        credits=3
    )

    Restriction.objects.create(
        subject=subject02,
        restriction=subject01,
    )

    Restriction.objects.create(
        subject=subject04,
        restriction=subject03,
    )

    Restriction.objects.create(
        subject=subject10,
        restriction=subject04,
    )

    Restriction.objects.create(
        subject=subject10,
        restriction=subject02,
    )

    course01 = Course.objects.create(
        subject=subject01,
        professor=professor01,
    )

    course02 = Course.objects.create(
        subject=subject02,
        professor=professor02,
    )

    course03 = Course.objects.create(
        subject=subject03,
        professor=professor03,
    )

    course04 = Course.objects.create(
        subject=subject04,
        professor=professor04,
    )

    course05 = Course.objects.create(
        subject=subject05,
        professor=professor01,
    )

    course06 = Course.objects.create(
        subject=subject06,
        professor=professor02,
    )

    course07 = Course.objects.create(
        subject=subject07,
        professor=professor03,
    )

    course08 = Course.objects.create(
        subject=subject08,
        professor=professor04,
    )

    course09 = Course.objects.create(
        subject=subject09,
        professor=professor01,
    )

    course10 = Course.objects.create(
        subject=subject10,
        professor=professor02,
    )

    inscription01 = Inscription.objects.create(
        student=student01,
        date='2021-01-01',
    )

    CourseInscription.objects.create(
        inscription=inscription01,
        course=course01,
        grade=4.5,
        status=CourseInscription.Status.APPROVED,
    )

    CourseInscription.objects.create(
        inscription=inscription01,
        course=course03,
        grade=3.5,
        status=CourseInscription.Status.APPROVED,
    )

    CourseInscription.objects.create(
        inscription=inscription01,
        course=course05,
        grade=2.5,
        status=CourseInscription.Status.REJECTED,
    )

    CourseInscription.objects.create(
        inscription=inscription01,
        course=course07,
        grade=1.5,
        status=CourseInscription.Status.REJECTED,
    )

    inscription02 = Inscription.objects.create(
        student=student02,
        date='2021-01-01',
    )

    CourseInscription.objects.create(
        inscription=inscription02,
        course=course02,
        grade=4.0,
        status=CourseInscription.Status.APPROVED,
    )

    CourseInscription.objects.create(
        inscription=inscription02,
        course=course04,
        grade=3.0,
        status=CourseInscription.Status.APPROVED,
    )

    CourseInscription.objects.create(
        inscription=inscription02,
        course=course06,
        grade=2.0,
        status=CourseInscription.Status.REJECTED,
    )

    CourseInscription.objects.create(
        inscription=inscription02,
        course=course08,
        grade=0.0,
        status=CourseInscription.Status.CANCELLED,
    )

    inscription03 = Inscription.objects.create(
        student=student03,
        date='2021-01-01',
    )

    CourseInscription.objects.create(
        inscription=inscription03,
        course=course09,
        grade=4.0,
        status=CourseInscription.Status.APPROVED,
    )

    CourseInscription.objects.create(
        inscription=inscription03,
        course=course10,
        grade=3.0,
        status=CourseInscription.Status.APPROVED,
    )

    CourseInscription.objects.create(
        inscription=inscription03,
        course=course03,
        grade=2.0,
        status=CourseInscription.Status.REJECTED,
    )

    CourseInscription.objects.create(
        inscription=inscription03,
        course=course05,
        grade=1.0,
        status=CourseInscription.Status.REJECTED,
    )

    inscription04 = Inscription.objects.create(
        student=student04,
        date='2021-07-01',
    )

    CourseInscription.objects.create(
        inscription=inscription04,
        course=course01,
    )

    CourseInscription.objects.create(
        inscription=inscription04,
        course=course02,
    )

    CourseInscription.objects.create(
        inscription=inscription04,
        course=course03,
    )

    CourseInscription.objects.create(
        inscription=inscription04,
        course=course04,
    )

    CourseInscription.objects.create(
        inscription=inscription04,
        course=course05,
    )

    inscription05 = Inscription.objects.create(
        student=student01,
        date='2021-07-01',
    )

    CourseInscription.objects.create(
        inscription=inscription05,
        course=course06,
    )

    CourseInscription.objects.create(
        inscription=inscription05,
        course=course07,
    )

    CourseInscription.objects.create(
        inscription=inscription05,
        course=course08,
    )

    CourseInscription.objects.create(
        inscription=inscription05,
        course=course09,
    )

    print('Database initialized!')


initialize_db()
