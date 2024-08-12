from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from grades.serializers import inscription
from grades.models import Course, Student, Inscription, CourseInscription, Subject, Restriction, CourseInscription


def student_meets_prerequisites(student: Student, subject: Subject) -> bool:
    prerequisite_subjects = Restriction.objects.filter(
        subject=subject).values_list('restriction', flat=True)
    if not prerequisite_subjects.exists():
        return True

    approved_subjects = CourseInscription.objects.filter(
        inscription__student=student, status=CourseInscription.Status.APPROVED).values_list('course__subject', flat=True)

    return all(prerequisite_subject in approved_subjects for prerequisite_subject in prerequisite_subjects)


@swagger_auto_schema(
    method='post',
    operation_summary='Create a inscription',
    operation_description='Create a inscription by passing a list of course ids',
    request_body=inscription.InscriptionCreationInputSerializer,
    responses={201: inscription.InscriptionCreationOutputSerializer}
)
@api_view(['POST'])
def create_inscription(request):
    student = Student.objects.filter(id=request.user.id).first()
    if student is None:
        return Response({'error': 'The user should be a student.'}, status=status.HTTP_400_BAD_REQUEST)

    input_serializer = inscription.InscriptionCreationInputSerializer(
        data=request.data)
    if not input_serializer.is_valid():
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    course_ids = input_serializer.data['course_ids']
    courses = Course.objects.filter(id__in=course_ids)
    if len(courses) != len(course_ids):
        return Response({'error': 'One or more courses do not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    prerequisite_errors = [
        f'Not meet prerequisites for course {course.subject.name}' for course in courses if not student_meets_prerequisites(student, course.subject)]
    if prerequisite_errors:
        return Response({'error': prerequisite_errors}, status=status.HTTP_400_BAD_REQUEST)

    new_inscription = Inscription.objects.create(student=student)

    CourseInscription.objects.bulk_create([CourseInscription(
        inscription=new_inscription, course=course) for course in courses])

    output = {'inscription_id': new_inscription.id, 'courses': courses}
    output_serializer = inscription.InscriptionCreationOutputSerializer(output)

    return Response(output_serializer.data, status=status.HTTP_201_CREATED)
