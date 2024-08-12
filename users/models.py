from django.contrib.auth.models import User


class Student(User):
    class Meta:
        verbose_name = 'Student'


class Professor(User):
    class Meta:
        verbose_name = 'Professor'
