from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, exceptions

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from grades.models import Student, Inscription, Subject
from grades.serializers.subject import ListCurrentSubjectSerializer


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
