import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import Professor, Student


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    credits = models.SmallIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class Restriction(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    restriction = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='restriction_subject')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['subject', 'restriction'], name='unique_subject_restriction')]

    def __str__(self) -> str:
        return f"Restriction {self.subject.name} - {self.restriction.name}"


class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['subject', 'professor'], name='unique_subject_professor')]

    def __str__(self):
        return f"Course {self.subject.name} - {self.professor.first_name} {self.professor.last_name}"


class Inscription(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['student', 'date'], name='unique_student_date')]

    def __str__(self):
        return f"Inscription {self.student.first_name} {self.student.last_name} - {self.date}"


class CourseInscription(models.Model):

    class Status(models.TextChoices):
        APPROVED = 'AP', 'Approved'
        REJECTED = 'RJ', 'Rejected'
        IN_PROGRESS = 'IP', 'In Progress'
        CANCELLED = 'CA', 'Cancelled'

    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.IN_PROGRESS)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['inscription', 'course'], name='unique_inscription_course')]

    def __str__(self):
        return f"Inscription Course {self.inscription.student.first_name} {self.inscription.student.last_name} - {self.course.subject.name} - {self.course.professor.first_name} {self.course.professor.last_name} - {self.inscription.date}"
