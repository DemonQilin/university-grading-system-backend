from django.db.models import F, Sum, ExpressionWrapper, FloatField
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, exceptions

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from grades.models import Student, Inscription, Subject, CourseInscription
from grades.serializers.subject import ListCurrentSubjectSerializer, StudentSummarySerializer


@swagger_auto_schema(
    method='get',
    operation_summary='List the current student subjects',
    operation_description='List of current subjects related to a student.',
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_PATH, type=openapi.TYPE_STRING,
                          description='The student username.', required=True)
    ],
    responses={200: ListCurrentSubjectSerializer(many=True)}
)
@api_view(['GET'])
def list_current_student_subjects(request, username):
    student = Student.objects.filter(username=username).first()
    if student is None:
        raise exceptions.NotFound({'error': 'Student not found.'})

    if student.id != request.user.id:
        raise exceptions.PermissionDenied(
            {'error': 'The student information is not available'})

    last_inscription = Inscription.objects.filter(
        student=student).order_by('-date').first()
    if last_inscription is None:
        raise exceptions.NotFound(
            {'error': 'The student has no inscriptions.'})

    subjects = Subject.objects.filter(
        course__courseinscription__inscription=last_inscription
    ).distinct()
    serializer = ListCurrentSubjectSerializer(subjects, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_summary='Get the student summary',
    operation_description='Summary of the student grades.',
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_PATH, type=openapi.TYPE_STRING,
                          description='The student username.', required=True)
    ],
    responses={200: StudentSummarySerializer}
)
@api_view(['GET'])
def get_student_summary(request, username):
    student = Student.objects.filter(username=username).first()
    if student is None:
        raise exceptions.NotFound({'error': 'Student not found.'})

    if student.id != request.user.id:
        raise exceptions.PermissionDenied(
            {'error': 'The student information is not available'})

    all_courses_inscriptions = CourseInscription.objects.filter(
        inscription__student=student
    ).distinct()

    weighted_average = all_courses_inscriptions.exclude(
        status__in=[CourseInscription.Status.IN_PROGRESS, CourseInscription.Status.CANCELLED]).annotate(
        weighted_grade=ExpressionWrapper(
            F('grade') * F('course__subject__credits'),
            output_field=FloatField()
        )
    ).aggregate(
        total_weighted_grade=Sum('weighted_grade'),
        total_credits=Sum('course__subject__credits')
    )

    if weighted_average['total_credits']:
        average = weighted_average['total_weighted_grade'] / \
            weighted_average['total_credits']
    else:
        average = 0.0

    approved = all_courses_inscriptions.filter(
        status=CourseInscription.Status.APPROVED)
    reprobated = all_courses_inscriptions.filter(
        status=CourseInscription.Status.REJECTED)
    canceled = all_courses_inscriptions.filter(
        status=CourseInscription.Status.CANCELLED)

    serializer = StudentSummarySerializer({
        'average': average,
        'approved': approved,
        'reprobated': reprobated,
        'canceled': canceled
    })

    return Response(serializer.data, status=status.HTTP_200_OK)
