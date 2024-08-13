from django.db.models import F, Sum, ExpressionWrapper, FloatField
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, exceptions

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from grades.models import Student, Inscription, Subject, CourseInscription, Professor, Course
from grades.serializers.subject import ListCurrentSubjectSerializer, StudentSummarySerializer, AssignGradeInputSerializer, StudentsBySubjectSerializer, StudentsBySubjectParamSerializer


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


@swagger_auto_schema(
    method='get',
    operation_summary='Get the professor subjects',
    operation_description='List of subjects related to a professor.',
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_PATH, type=openapi.TYPE_STRING,
                          description='The professor username.', required=True)
    ],
)
@api_view(['GET'])
def get_professor_subjects(request, username):
    professor = Professor.objects.filter(username=username).first()
    if professor is None:
        raise exceptions.NotFound({'error': 'Professor not found.'})

    if professor.id != request.user.id:
        raise exceptions.PermissionDenied(
            {'error': 'The professor information is not available'})

    subjects = Subject.objects.filter(
        course__professor=professor
    ).distinct()

    serializer = ListCurrentSubjectSerializer(subjects, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='patch',
    operation_summary='Assign a grade to a student',
    operation_description='Assign a grade to a student in a course.',
    manual_parameters=[
        openapi.Parameter('course_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                          description='The course id.', required=True)
    ],
    request_body=AssignGradeInputSerializer,
    responses={200: openapi.Response(
        description='Grade assigned successfully.')}
)
@api_view(['PATCH'])
def assign_course_grade(request, course_id):
    course = Course.objects.filter(id=course_id).first()
    if course is None:
        raise exceptions.NotFound({'error': 'Course not found.'})

    if course.professor.id != request.user.id:
        raise exceptions.PermissionDenied(
            {'error': 'Only the professor can assign grades.'})

    input_serializer = AssignGradeInputSerializer(data=request.data)
    if not input_serializer.is_valid():
        raise exceptions.ValidationError(input_serializer.errors)

    data = input_serializer.data
    student = Student.objects.filter(username=data['student']).first()
    if student is None:
        raise exceptions.NotFound({'error': 'Student not found.'})

    course_inscription = CourseInscription.objects.filter(
        inscription__student=student,
        course=course,
        status=CourseInscription.Status.IN_PROGRESS
    ).order_by('-inscription__date').first()

    if course_inscription is None:
        raise exceptions.NotFound(
            {'error': 'Student is not enrolled in the course.'})

    course_inscription.grade = data['grade']
    course_inscription.status = CourseInscription.Status.APPROVED if data[
        'grade'] >= 3 else CourseInscription.Status.REJECTED
    course_inscription.save()

    return Response({'message': 'Grade assigned successfully.'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_summary='Get the students by subject',
    operation_description='List of students related to a subject.',
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_PATH, type=openapi.TYPE_STRING,
                          description='The professor username.', required=True),
        openapi.Parameter('subject_id', openapi.IN_PATH, type=openapi.TYPE_STRING,
                          description='The subject id.', required=True),
        openapi.Parameter('current', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                          description='Filter by students in progress', required=False, default=False)
    ],
    responses={200: StudentsBySubjectSerializer(many=True)}
)
@api_view(['GET'])
def get_students_by_subject(request, username, subject_id):
    professor = Professor.objects.filter(username=username).first()
    if professor is None:
        raise exceptions.NotFound({'error': 'Professor not found.'})

    if professor.id != request.user.id:
        raise exceptions.PermissionDenied(
            {'error': 'The professor information is not available'})

    subject = Subject.objects.filter(id=subject_id).first()
    if subject is None:
        raise exceptions.NotFound({'error': 'Subject not found.'})

    course = Course.objects.filter(
        professor=professor, subject=subject).first()
    if course is None:
        raise exceptions.PermissionDenied(
            {'error': 'The professor is not related to the subject.'})

    params_serializer = StudentsBySubjectParamSerializer(
        data=request.query_params)
    if not params_serializer.is_valid():
        raise exceptions.ValidationError(params_serializer.errors)

    course_inscriptions = CourseInscription.objects.filter(
        course=course
    ).distinct()

    if params_serializer.data['current']:
        course_inscriptions = course_inscriptions.filter(
            status=CourseInscription.Status.IN_PROGRESS)

    serializer = StudentsBySubjectSerializer(course_inscriptions, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
