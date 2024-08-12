from django.utils.decorators import method_decorator
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

from grades.models import Course
from grades.serializers import course


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='List all courses',
    operation_description='List of subjects related to the professors who teach them.',
    responses={200: course.ListCourseSerializer(many=True)}
))
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = course.ListCourseSerializer
