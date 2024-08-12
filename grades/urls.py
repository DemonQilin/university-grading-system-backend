from django.urls import path

from grades.views import course

app_name = 'grades'

urlpatterns = [
    path('courses/', course.CourseListView.as_view(), name='course_list')
]
